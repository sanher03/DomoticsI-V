import argparse

from .switch import Switch


parser = argparse.ArgumentParser(
                    prog='Dummy switch script',
                    description='Ejecutable que instancia un interruptor')


parser.add_argument("--host", dest="host", metavar="<hostname>", type=str, default="test.mosquitto.org", help="Nombre del host a conectarse")
parser.add_argument("-p", "--port", dest="port", metavar="<port>", type=int, default=1883, help="Puerto en el que recibir la conexión")
parser.add_argument("-P", "--probability", dest="prob", metavar="<probability of failing>", type=float, default=1, help="Probalidad de fallo al recibir una acción (Default: 0.3)")
parser.add_argument('id', type=int, help='ID del dispositivo')

args = parser.parse_args()

print(args.host)
print(args.port)
print(args.prob)
print(args.id)

switch = Switch(args.host, args.port, args.prob, args.id)

switch.start()
    
    