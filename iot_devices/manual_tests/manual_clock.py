import sys, os, argparse, datetime
from iot_devices.clock import Clock
from datetime import date, datetime, timedelta, time
import time

def str_a_datetime(cadena_hora):
    return datetime.strptime(cadena_hora, "%H:%M:%S").time()


parser = argparse.ArgumentParser(
                    prog='Test clock script',
                    description='Ejecutable que testea un reloj')


parser.add_argument("--host", dest="host", metavar="<hostname>", type=str, default="test.mosquitto.org", help="Nombre del host a conectarse (Default: redes2.ii.uam.es)")
parser.add_argument("-p", "--port", dest="port", metavar="<port>", type=int, default=1883, help="Puerto en el que recibir la conexión (Default: 1883)")
parser.add_argument("--time", dest="time", metavar="<HH:MM:SS>", type=str_a_datetime, default=datetime.now().time(), help="Intervalo en segundos que tarda en simular un cambio de estado (Deafult: Hora Actual)")
parser.add_argument("--increment", dest="increment", metavar="<incremento>", type=int, default=1, help="Incremento entre envíos en segundos (Default: 1)")
parser.add_argument("--rate", dest="rate", metavar="<rate>", type=int, default=1, help="Frecuencia de envío en segundos (Default: 1)")
parser.add_argument('id', type=int, help='ID del dispositivo')

command_test = "--host test.mosquitto.org --port 1883 --time 09:00:00 --increment 10 --rate 2 3"

print(f"\nProcedemos a parsear la cadena: {command_test}")

args = parser.parse_args(command_test.split(" "))

print("\nSe está haciendo uso de los siguientes argumentos:")
print("\t- Host: " + args.host)
print("\t- Port: " + str(args.port))
print("\t- Time: " + str(args.time))
print("\t- Increment: " + str(args.increment))
print("\t- Rate: " + str(args.rate))
print("\t- Id: " + str(args.id))

print("\nProcedemos a instanciar un sensor")

clock = Clock(args.host, args.port, args.time, args.increment, args.rate, args.id)

print("\nProcedemos a iniciar el bucle de envíos del reloj, pulse (Control + C) para finalizar el test\n")

clock.start()

print("\nTest terminado")