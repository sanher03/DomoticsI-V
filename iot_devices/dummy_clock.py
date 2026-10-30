import argparse
from datetime import datetime

from .clock import Clock

def str_a_datetime(cadena_hora):
    return datetime.strptime(cadena_hora, "%H:%M:%S").time()

parser = argparse.ArgumentParser(
                    prog='Dummy clock script',
                    description='Ejecutable que instancia un reloj')


parser.add_argument("--host", dest="host", metavar="<hostname>", type=str, default="test.mosquitto.org", help="Nombre del host a conectarse")
parser.add_argument("-p", "--port", dest="port", metavar="<port>", type=int, default=1883, help="Puerto en el que recibir la conexión")
parser.add_argument("--time", dest="time", metavar="<HH:MM:SS>", type=str_a_datetime, default=datetime.now().time(), help="Intervalo en segundos que tarda en simular un cambio de estado (Deafult: Hora Actual)")
parser.add_argument("--increment", dest="increment", metavar="<incremento>", type=int, default=1, help="Incremento entre envíos en segundos (Default: 1)")
parser.add_argument("--rate", dest="rate", metavar="<rate>", type=int, default=1, help="Frecuencia de envío en segundos (Default: 1)")
parser.add_argument('id', type=int, help='ID del dispositivo')

args = parser.parse_args()

print(args.host)
print(args.port)
print(args.time)
print(args.increment)
print(args.rate)
print(args.id)

clock = Clock(args.host, args.port, args.time, args.increment, args.rate, args.id)

clock.start()

print("Programa terminado")
    