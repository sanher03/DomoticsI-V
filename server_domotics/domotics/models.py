from django.db import models
from django.forms import ValidationError
from devices.models import Device
from rules.models import Rule
# Create your models here.

    
class Event(models.Model):
    STATE = [
        ('QUERY', 'Query'),
        ('CHANGE', 'Change'),
    ]
    STATUS = [
        ('SUCCEDED', 'Succeded'),
        ('FAILED', 'Failed'),
    ]
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    state = models.CharField(max_length=200, choices=STATE)
    value = models.CharField(max_length=200)
    read = models.BooleanField(default=False)
    status = models.CharField(max_length=200, choices=STATUS, default='SUCCEDED')
    
    
    