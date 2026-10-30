from django.db import models
from django.forms import ValidationError
# Create your models here.

class Device(models.Model):
    DEVICE_TYPE = [
        ('SENSOR', 'Sensor'),
        ('SWITCH', 'Interruptor'),
        ('CLOCK', 'Reloj'),
    ]
    
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=DEVICE_TYPE, name="type", default='SENSOR')
    
    def __str__(self):
        return self.name
    
    
    def clean(self):
        if len(self.name) < 4:
            raise ValueError("El nombre debe tener al menos 3 caracteres")
        if self.id <= 0:
            raise ValueError("El identificador debe ser positivo")
    