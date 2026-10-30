from django import forms
from .models import Device

class NewDevice(forms.ModelForm):
    class Meta:
        model = Device
        fields = '__all__'  # O puedes especificar los campos específicos que deseas incluir en el formulario

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['type'].widget = forms.RadioSelect(choices=self.fields['type'].widget.choices, attrs={'class': 'form-check-input'})