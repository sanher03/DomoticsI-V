import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server_domotics.settings")
django.setup()

from domotics.models import Device, Event, Rule
from django.core.exceptions import ObjectDoesNotExist

try:
    obj = Device.objects.get(id=1)
    obj.delete()
    print("Objeto eliminado exitosamente.")
except ObjectDoesNotExist:
    print("El objeto no existe en la base de datos.")

t1 = Device(id=1, name="switch", type = 'SWITCH')
t1.save()

try:
    obj = Device.objects.get(id=2)
    obj.delete()
    print("Objeto eliminado exitosamente.")
except ObjectDoesNotExist:
    print("El objeto no existe en la base de datos.")

t2 = Device(id=2, name="sensor", type = 'SENSOR')
t2.save()

try:
    obj = Device.objects.get(id=3)
    obj.delete()
    print("Objeto eliminado exitosamente.")
except ObjectDoesNotExist:
    print("El objeto no existe en la base de datos.")

t3 = Device(id=3, name="reloj", type = 'CLOCK')
t3.save()

obj = Rule.objects.filter(device1=t2)
if obj:
    obj.delete()
    print("Objeto(s) eliminado exitosamente.")

t4 = Rule(name='Regla1', device1=t2, comparator='EQUALS', value="20", device2=t1, turn_on=True)
t4.save()

obj = Rule.objects.filter(device1=t3)
if obj:
    obj.delete()
    print("Objeto(s) eliminado exitosamente.")

t5 = Rule(device1=t3, comparator='EQUALS', value="09:03:00", device2=t1, turn_on=False)
t5.save()