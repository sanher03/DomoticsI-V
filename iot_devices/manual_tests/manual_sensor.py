import sys, os, argparse
from iot_devices.sensor import Sensor

parser = argparse.ArgumentParser(
                    prog='Dummy sensor script',
                    description='Ejecutable que instancia un sensor')


parser.add_argument("--host", dest="host", metavar="<hostname>", type=str, default="test.mosquitto.org", help="Nombre del host a conectarse (Default: redes2.ii.uam.es)")
parser.add_argument("-p", "--port", dest="port", metavar="<port>", type=int, default=1883, help="Puerto en el que recibir la conexión (Default: 1883)")
parser.add_argument("-i", "--interval", dest="interval", metavar="<intervalo>", type=int, default=1, help="Intervalo en segundos que tarda en simular un cambio de estado (Deafult: 1)")
parser.add_argument("-m", "--min", dest="min", metavar="<minimo>", type=int, default=20, help="Valor mínimo a enviar (Default: 20)")
parser.add_argument("-M", "--max", dest="max", metavar="<maximo>", type=int, default=30, help="Valor máximo a enviar (Default: 30)")
parser.add_argument("--increment", dest="increment", metavar="<incremento>", type=int, default=1, help="Incremento entre el mínimo y el máximo (Default: 1)")
parser.add_argument('id', type=int, help='ID del dispositivo')

command_test = "--host test.mosquitto.org --port 1883 --interval 1 --min 10 --max 30 --increment 2 2"

print(f"\nProcedemos a parsear la cadena: {command_test}")

args = parser.parse_args(command_test.split(" "))

print("\nSe está haciendo uso de los siguientes argumentos:")
print("\t- Host: " + args.host)
print("\t- Port: " + str(args.port))
print("\t- Interval: " + str(args.interval))
print("\t- Minimum: " + str(args.min))
print("\t- Maximum: " + str(args.max))
print("\t- Increment: " + str(args.increment))
print("\t- Id: " + str(args.id))

print("\nProcedemos a instanciar un sensor")

sensor = Sensor(args.host, args.port, args.min, args.max, args.increment, args.interval, args.id)

print("\nProcedemos a iniciar el bucle de envíos del sensor, pulse (Control + C) para finalizar el test\n")

sensor.start()

print("\nTest terminado")