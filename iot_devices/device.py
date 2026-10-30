import paho.mqtt.client as mqtt
from abc import ABC, abstractmethod

class Device(ABC):
    def __init__(self, host, port, value, id):
        self.host = host
        self.port = port
        self.value = value
        self.id = id
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
        
    @abstractmethod
    def on_connect(self, client, userdata, flags, reason_code, properties):
        pass
    
    @abstractmethod
    def signal_handler(self, signal, frame):
        pass
    
    @abstractmethod
    def start(self):
        pass
    
    
        
    
        
    
