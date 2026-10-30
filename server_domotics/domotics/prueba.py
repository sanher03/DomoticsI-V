import os
import django
import sys
sys.path.append('../')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server_domotics.settings")
django.setup()

from devices import models
from rules import models
from domotics import models




t = models.Event(device=models.Device.objects.get(id=30), state="QUERY", value="21", read=False)
t.save()
t = models.Event(device=models.Device.objects.get(id=25), state="CHANGE", value="ON", read=False)
t.save()


