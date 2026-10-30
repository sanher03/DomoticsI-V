from datetime import date, datetime, timedelta, time
from .device import Device
import time, signal


class Clock(Device):
    def __init__(self, host, port, time, incr, rate, id):
        super().__init__(host, port, time, id)

        self.time = time
        self.incr = incr
        self.rate = rate
        self.loop = True

    def on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code.is_failure:
            print(
                f"Failed to connect: {reason_code}."
            )
        else:
            # we should always subscribe from on_connect callback to be sure
            # our subscribed is persisted across reconnections.
            print("Sucesfully connected to the broker")
            
    def signal_handler(self, signal, frame):
        print('You pressed Ctrl+C!')
        print("Ending clock")
        self.loop = False
        self.mqttc.disconnect()

    def start(self):
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_subscribe = self.on_subscribe
        self.mqttc.on_unsubscribe = self.on_unsubscribe
        signal.signal(signal.SIGINT, self.signal_handler)

        self.mqttc.connect(self.host, self.port)
        self.mqttc.loop_start()
        
        incremento = timedelta(seconds=self.incr)
        tiempo_actual = datetime.combine(date.today(), self.time)
        
        while self.loop:
            msg_info = self.mqttc.publish("redes/2313/05/" + str(self.id), "value " + tiempo_actual.time().isoformat())
            msg_info.wait_for_publish()
            print(tiempo_actual.time().isoformat(timespec="seconds"))
            tiempo_actual += incremento
            time.sleep(1 / self.rate)
                 
