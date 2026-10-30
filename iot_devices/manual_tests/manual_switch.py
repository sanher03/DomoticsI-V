import sys, os, argparse, time
from iot_devices.switch import Switch
from iot_devices.switch_state import SwitchState


parser = argparse.ArgumentParser(
                    prog='Test switch script',
                    description='Ejecutable que testea un interruptor')


parser.add_argument("--host", dest="host", metavar="<hostname>", type=str, default="test.mosquitto.org", help="Nombre del host a conectarse (Default: redes2.ii.uam.es)")
parser.add_argument("-p", "--port", dest="port", metavar="<port>", type=int, default=1883, help="Puerto en el que recibir la conexión (Default: 1883)")
parser.add_argument("-P", "--probability", dest="prob", metavar="<probability of failing>", type=float, default=1, help="Probalidad de fallo al recibir una acción (Default: 0.3)")
parser.add_argument('id', type=int, help='ID del dispositivo')

command_test = "--host test.mosquitto.org --port 1883 --probability 0.99 1"

print(f"\nProcedemos a parsear la cadena: {command_test}")

args = parser.parse_args(command_test.split(" "))

print("\nSe está haciendo uso de los siguientes argumentos:")
print("\t- Host: " + args.host)
print("\t- Port: " + str(args.port))
print("\t- Probability: " + str(args.prob))
print("\t- Id: " + str(args.id))

print("\nProcedemos a instanciar un interruptor")

switch = Switch(args.host, args.port, args.prob, args.id)

print("\nEstado inicial del interruptor: " + str(switch.value))

print("\nConectamos el interruptor al broker: ")

switch.mqttc.on_connect = switch.on_connect
switch.mqttc.on_subscribe = switch.on_subscribe
switch.mqttc.on_message = switch.on_message

switch.mqttc.connect(args.host, args.port)

switch.mqttc.loop_start()

time.sleep(1)

print("\nEntrando en un bucle generador de eventos, para salir introduzca \"e\":")

s = "\n"
i = 0;

print("\nInterruptor en estado " + str(switch.value) + ", introduzca cualquier letra para cambiar a estado " + str(SwitchState(i)))
s = input(">> ")

while s != "e":
    
    msg = switch.mqttc.publish("redes/2313/05/" + str(switch.id) + "/set", "change " + str(SwitchState(i)))
    msg.wait_for_publish()
    
    #Espera para dejar actuar a la función de callback
    time.sleep(1)
    
    if (str(switch.value) != str(SwitchState(i))):
        print("\nNo se ha podido cambiar de estado, debido a la probalidad de fallo al recibir una acción")
    else:
        i += 1
        i = i % 2
    
    print("\nInterruptor en estado " + str(switch.value) + ", introduzca cualquier letra para cambiar a estado " + str(SwitchState(i)))
    s = input(">> ")
    
    
print("\nDesconectando switch del broker")

switch.mqttc.disconnect()

print("\nTest terminado")
    




