from enum import Enum
import os, django
from datetime import time
import sys
sys.path.append('../')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server_domotics.settings")
django.setup()

from domotics.models import Rule, Device
from django.core.exceptions import ObjectDoesNotExist


class RuleEngine:
    """
    Definicion de un repartidor.

    Args:
        rules: Lista con las reglas definidas

    """

    def __init__(self):
        self.rules = []

    def accept_rule(self, device: Device, value):
        
        list_events = []
        
        rules_filtradas = Rule.objects.filter(device1=device)
        
        if not rules_filtradas.exists():
            # Manejar el caso en que no se encontró ningún objeto que coincida con los criterios de búsqueda
            print("No existen reglas asociadas a este dispositivo")
        else:
            # Hacer algo con los rules encontradas
            for rule in rules_filtradas:
                if device.type == 'SWITCH':
                    value_of_rule = eval(rule.value)
                elif device.type == 'SENSOR':
                    value_of_rule = int(rule.value)
                elif device.type == 'CLOCK':
                    value_of_rule = time.fromisoformat(rule.value)
                    
                    
                if rule.comparator == 'MORE_THAN':
                    if value > value_of_rule:
                        list_events.append((rule.device2.id, rule.turn_on))
                elif rule.comparator == 'LESS_THAN':
                    if value < value_of_rule:
                        list_events.append((rule.device2.id, rule.turn_on))
                elif rule.comparator == 'EQUALS':
                    if value == value_of_rule:
                        list_events.append((rule.device2.id, rule.turn_on))
                        
        return list_events
            
