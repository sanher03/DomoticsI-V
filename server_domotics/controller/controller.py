from .rule_engine import RuleEngine
import paho.mqtt.client as mqtt
from datetime import time as timed
import argparse, time, os, django, signal, traceback
from iot_devices.switch_state import SwitchState
import sys
sys.path.append('../')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server_domotics.settings")
django.setup()


from domotics.models import Device, Event
from django.core.exceptions import ObjectDoesNotExist


class Controller():
    """
    Definicion de un repartidor.

    Args:
        rule_engine: Conjunto de reglas definidas
        devices: Dispositivos registrados
        host: Nombre del host MQTT a donde conectarse

    """
    def __init__(self, host, port):
        self.rule_engine = RuleEngine()
        self.host = host
        self.port = port
        self.mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    def on_subscribe(self, client, userdata, mid, reason_code_list, properties):
        # Since we subscribed only for a single channel, reason_code_list contains
        # a single entry
        if reason_code_list[0].is_failure:
            print(f"Broker rejected you subscription: {reason_code_list[0]}")
        else:
            print(f"Broker granted the following QoS: {reason_code_list[0].value}")

    def on_unsubscribe(self, client, userdata, mid, reason_code_list, properties):
        # Be careful, the reason_code_list is only present in MQTTv5.
        # In MQTTv3 it will always be empty

        if len(reason_code_list) == 0 or not reason_code_list[0].is_failure:
            print("unsubscribe succeeded (if SUBACK is received in MQTTv3 it success)")
        else:
            print(f"Broker replied with failure: {reason_code_list[0]}")
        client.disconnect()

    def on_message(self, client, userdata, message):
        body = message.payload.decode()
        topic_split = message.topic.split("/")

        if topic_split[len(topic_split) - 1] == "set":
            id = int(topic_split[len(topic_split) - 2])
        else:
            id = int(topic_split[len(topic_split) - 1])

        print("Message received: ", message.payload.decode())
        body_split = body.split(" ")

        if body_split[0].startswith("value"):
            try:

                device = Device.objects.get(id=id)
                
                if len(body_split) == 2:
                
                    if body_split[0] == 'value_query':
                        ev = Event(device=Device.objects.get(id=id), state='QUERY', value=str(body_split[1]))
                        ev.save()

                    if device.type == "SWITCH":
                        value = eval(body_split[1])
                    elif device.type == "SENSOR":
                        value = int(body_split[1])
                    elif device.type == "CLOCK":
                        value = timed.fromisoformat(body_split[1])
                                            
                    list_events = self.rule_engine.accept_rule(device, value)

                    if list_events:
                        print("Events found")
                        for event in list_events:
                            if event[1]:
                                value_change = SwitchState.ON
                            else:
                                value_change = SwitchState.OFF
                            self.mqttc.publish(
                                "redes/2313/05/" + str(event[0]) + "/set", "change " + str(value_change), qos=1
                            )
                            print("Publishing \"change " + str(value_change) + "\"")
                            
                elif len(body_split) == 3:
                    ev = Event(device=Device.objects.get(id=id), state='CHANGE', value=body_split[1], status=body_split[2])
                    ev.save()

            except ObjectDoesNotExist:
                print("El dispositivo no está registrado, se ignoró el mensaje")
        
        elif body_split[0] == 'view_consult':
            self.consultar_estado(int(body_split[1]))

    def on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code.is_failure:
            print(
                f"Failed to connect: {reason_code}. loop_forever() will retry connection"
            )
        else:
            # we should always subscribe from on_connect callback to be sure
            # our subscribed is persisted across reconnections.
            print("Connection was succesful.")
            client.subscribe("redes/2313/05/#")

    def consultar_estado(self, id_device):
        print("consultar")
        try:
            device = Device.objects.get(id=id_device)

            if device.type == "SWITCH" or device.type == "SENSOR":
                self.mqttc.publish(
                    "redes/2313/05/" + str(id_device), "consult", qos=1
                )
            else:
                print("Sólo se puede consultar el estado de interruptores y sensores")                   
            

        except ObjectDoesNotExist:
            print("El dispositivo no está registrado, no se puede consultar su estado")
            
    def signal_handler(self, signal, frame):
        print('You pressed Ctrl+C!')
        print("I will wait for all threads... waiting to be finished")
        self.mqttc.unsubscribe("redes/2313/05/#")
        
    def listen(self):
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_message = self.on_message
        self.mqttc.on_subscribe = self.on_subscribe
        self.mqttc.on_unsubscribe = self.on_unsubscribe
        signal.signal(signal.SIGINT, self.signal_handler)

        self.mqttc.connect(self.host, self.port)
        self.mqttc.loop_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Dummy clock script", description="Ejecutable que instancia un reloj"
    )

    parser.add_argument(
        "--host",
        dest="host",
        metavar="<hostname>",
        type=str,
        default=os.environ.get("MQTT_HOST", "test.mosquitto.org"),
        help="Nombre del host a conectarse",
    )
    parser.add_argument(
        "-p",
        "--port",
        dest="port",
        metavar="<port>",
        type=int,
        default=int(os.environ.get("MQTT_PORT", "1883")),
        help="Puerto en el que recibir la conexión",
    )

    args = parser.parse_args()


    print(args.host)
    print(args.port)

    controller = Controller(args.host, args.port)

    controller.listen()
