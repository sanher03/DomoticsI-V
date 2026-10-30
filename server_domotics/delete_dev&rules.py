import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server_domotics.settings")
django.setup()

from domotics.models import Device, Event, Rule
from django.core.exceptions import ObjectDoesNotExist

events = Event.objects.all()

for event in events:
    print(f"Device_changed: {event.device}, State: {event.state}, Value: {event.value}, Status: {event.status}")

try:
    obj = Device.objects.get(id=1)
    obj.delete()
    print("Objeto eliminado exitosamente.")
except ObjectDoesNotExist:
    print("El objeto no existe en la base de datos.")

try:
    obj = Device.objects.get(id=2)
    obj.delete()
    print("Objeto eliminado exitosamente.")
except ObjectDoesNotExist:
    print("El objeto no existe en la base de datos.")
    
try:
    obj = Device.objects.get(id=3)
    obj.delete()
    print("Objeto eliminado exitosamente.")
except ObjectDoesNotExist:
    print("El objeto no existe en la base de datos.")


