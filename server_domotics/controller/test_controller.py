import argparse
import os
import time

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server_domotics.settings")
django.setup()

from controller.controller import Controller
from domotics.models import Device, Event, Rule


def main():
    parser = argparse.ArgumentParser(
        prog="Test controller script",
        description="Ejecutable que testea el controlador",
    )
    parser.add_argument(
        "--host",
        default="test.mosquitto.org",
        help="Nombre del host a conectarse",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=1883,
        help="Puerto en el que recibir la conexión",
    )
    args = parser.parse_args()

    controller = Controller(args.host, args.port)
    switch = Device.objects.update_or_create(
        id=1, defaults={"name": "switch1", "type": "SWITCH"}
    )[0]
    sensor = Device.objects.update_or_create(
        id=2, defaults={"name": "sensor1", "type": "SENSOR"}
    )[0]
    Rule.objects.filter(device1=sensor).delete()
    Rule.objects.create(
        name="hola",
        device1=sensor,
        comparator="EQUALS",
        value="20",
        device2=switch,
        turn_on=True,
    )

    controller.mqttc.on_connect = controller.on_connect
    controller.mqttc.on_message = controller.on_message
    controller.mqttc.on_subscribe = controller.on_subscribe
    controller.mqttc.on_unsubscribe = controller.on_unsubscribe
    controller.mqttc.connect(args.host, args.port)
    controller.mqttc.loop_start()

    time.sleep(1)
    controller.mqttc.publish("redes/2313/05/2", "value 20").wait_for_publish()
    time.sleep(1)
    controller.mqttc.publish(
        "redes/2313/05/1", "value_change SwitchState.ON SUCCEDED"
    ).wait_for_publish()
    time.sleep(1)
    controller.mqttc.publish("redes/2313/05/3", "value 20").wait_for_publish()
    time.sleep(1)
    controller.mqttc.unsubscribe("redes/2313/05/#")

    for event in Event.objects.all():
        print(
            f"Device_changed: {event.device}, State: {event.state}, "
            f"Value: {event.value}, Status: {event.status}"
        )

    Device.objects.filter(id__in=[1, 2]).delete()


if __name__ == "__main__":
    main()
