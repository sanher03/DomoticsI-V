import argparse

from .sensor import Sensor

parser = argparse.ArgumentParser(
                    prog='Dummy sensor script',
                    description='Ejecutable que instancia un sensor')


parser.add_argument("--host", dest="host", metavar="<hostname>", type=str, default="test.mosquitto.org", help="Nombre del host a conectarse")
parser.add_argument("-p", "--port", dest="port", metavar="<port>", type=int, default=1883, help="Puerto en el que recibir la conexión")
parser.add_argument("-i", "--interval", dest="interval", metavar="<intervalo>", type=int, default=1, help="Intervalo en segundos que tarda en simular un cambio de estado (Deafult: 1)")
parser.add_argument("-m", "--min", dest="min", metavar="<minimo>", type=int, default=20, help="Valor mínimo a enviar (Default: 20)")
parser.add_argument("-M", "--max", dest="max", metavar="<maximo>", type=int, default=30, help="Valor máximo a enviar (Default: 30)")
parser.add_argument("--increment", dest="increment", metavar="<incremento>", type=int, default=1, help="Incremento entre el mínimo y el máximo (Default: 1)")
parser.add_argument('id', type=int, help='ID del dispositivo')

args = parser.parse_args()

print(args.host)
print(args.port)
print(args.interval)
print(args.min)
print(args.max)
print(args.increment)
print(args.id)

sensor = Sensor(args.host, args.port, args.min, args.max, args.increment, args.interval, args.id)

sensor.start()

print("Programa terminado")
    
    