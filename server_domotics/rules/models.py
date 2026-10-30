from django.db import models
from devices.models import Device
from datetime import time
# Create your models here.
class Rule(models.Model):
    COMPARATOR_TYPE = [
        ('MORE_THAN', 'Mayor que'),
        ('LESS_THAN', 'Menor que'),
        ('EQUALS', 'Igual a'),
    ]
    name = models.CharField(max_length=200)
    device1 = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="device_cause")
    comparator = models.CharField(max_length=20, choices=COMPARATOR_TYPE)
    value = models.CharField(max_length=200)
    device2 = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="device_to_change")
    turn_on = models.BooleanField()
    
    def clean(self):
        if len(self.name) < 4:
            raise ValueError("El nombre debe tener al menos 3 caracteres")
        if self.device1.type == "CLOCK":
            try:
                time.fromisoformat(self.value)
                
            except ValueError:
                raise ValueError("El valor debe ser una hora en este formato: 'HH:MM:SS'")
        if self.device1.type == 'SENSOR':
            try:
                numero = int(self.value)
            except ValueError:
                raise ValueError("El valor debe ser un numero entero correspondiente al sensor")
        if self.device1.type == 'SWITCH':
            raise ValueError("El dispositivo causante no puede ser un interruptor")