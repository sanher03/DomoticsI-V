from .device import Device
from .switch_state import SwitchState
import random, signal

class Switch(Device):
    def __init__(self, host, port, probability, id):
        super().__init__(host, port, SwitchState.OFF, id)
        
        self.probability = probability
        
    
    def on_message(self, client, userdata, message):
        body = message.payload.decode()
        topic_split = message.topic.split('/')
    
        
        if topic_split[len(topic_split) - 1] == "set":
            body_split = body.split(" ")
            if (body_split[0] == "change"):
                if self.value == eval(body_split[1]):
                    return
                rand_num = random.random()
                if rand_num <= self.probability:
                    self.value = eval(body_split[1])
                    print("State changed to " + str(self.value))
                    self.mqttc.publish("redes/2313/05/" + str(self.id) + "/set", "value_change " + str(self.value) + " SUCCEDED", qos=1)
                else:
                    self.mqttc.publish("redes/2313/05/" + str(self.id) + "/set", "value_change " + body_split[1] + " FAILED", qos=1)
        else:
            if (body == "consult"):
                self.mqttc.publish("redes/2313/05/" + str(self.id), "value_query " + str(self.value), qos=1)
            
            
    def on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code.is_failure:
            print(f"Failed to connect: {reason_code}.")
        else:
            # we should always subscribe from on_connect callback to be sure
            # our subscribed is persisted across reconnections.
            print("Connection was succesful.")
            client.subscribe("redes/2313/05/" + str(self.id) + "/#")
            
    def signal_handler(self, signal, frame):
        print('You pressed Ctrl+C!')
        print("Ending switch")
        self.mqttc.unsubscribe("redes/2313/05/" + str(self.id) + "/#")
            
        
    def start(self):
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_message = self.on_message
        self.mqttc.on_subscribe = self.on_subscribe
        self.mqttc.on_unsubscribe = self.on_unsubscribe
        signal.signal(signal.SIGINT, self.signal_handler)
        
        self.mqttc.connect(self.host, self.port)
        
        self.mqttc.loop_forever()
        
        print(f"Received the following message: {self.mqttc.user_data_get()}")
