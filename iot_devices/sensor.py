import time
from .device import Device
import signal

class Sensor(Device):
    def __init__(self, host, port, min, max, incr, interval, id):
        super().__init__(host, port, min, id)

        self.min = min
        self.max = max
        self.incr = incr
        self.interval = interval
        self.loop = True

    def on_message(self, client, userdata, message):
        body = message.payload.decode()

        if (body == "consult"):
            self.mqttc.publish("redes/2313/05/" + str(self.id), "value_query " + str(self.value), qos=1)

        
    def on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code.is_failure:
            print(f"Failed to connect: {reason_code}.")
        else:
            # we should always subscribe from on_connect callback to be sure
            # our subscribed is persisted across reconnections.
            print("Connection was succesful.")
            client.subscribe("redes/2313/05/" + str(self.id))
            
    def signal_handler(self, signal, frame):
        print('You pressed Ctrl+C!')
        print("Ending sensor")
        self.loop = False
        self.mqttc.unsubscribe("redes/2313/05/" + str(self.id))


    def start(self):
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_message = self.on_message
        self.mqttc.on_subscribe = self.on_subscribe
        self.mqttc.on_unsubscribe = self.on_unsubscribe
        signal.signal(signal.SIGINT, self.signal_handler)

        self.mqttc.connect(self.host, self.port)
        self.mqttc.loop_start()

        while self.loop:
            msg_info = self.mqttc.publish("redes/2313/05/" + str(self.id), "value " + str(self.value))
            msg_info.wait_for_publish()
            print("Valor enviado:", self.value)
            print("en el topic:" + "redes/2313/05/" + str(self.id))
            self.value += self.incr
            if self.value > self.max:
                self.value = self.min
            time.sleep(self.interval)
        
        

