from django import forms
from .models import Rule
from devices import models
from itertools import chain


class CustomBooleanRadioWidget(forms.RadioSelect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = (
            (True, 'Encender'),
            (False, 'Apagar'),
        )
        
class NewRule(forms.ModelForm):
    class Meta:
        model = Rule
        fields = '__all__'  # O puedes especificar los campos específicos que deseas incluir en el formulario
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['turn_on'].widget = CustomBooleanRadioWidget()
        
        self.fields['device2'].queryset = models.Device.objects.filter(type='SWITCH')
        
        
        
