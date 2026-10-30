from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from .models import Device
from .forms import NewDevice
import paho.mqtt.client as mqtt

# Create your views here.

def devices(request):
    device_list = Device.objects.all()
    return render(request, "device.html", {"element_list": device_list})


def delete_device(request, id):
    Device.objects.get(id=id).delete()
    return JsonResponse({'cambio': True})

def consult_device(request, id):
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.connect(settings.MQTT_HOST, settings.MQTT_PORT)
    mqttc.loop_start()
    msg = mqttc.publish("redes/2313/05/views/15", "view_consult " + str(id))
    msg.wait_for_publish()
    mqttc.disconnect()
    mqttc.loop_stop()
    return JsonResponse({})
            

def add_device(request):
    if request.method == 'POST':
        formulario = NewDevice(request.POST)
        
        try:
            
            formulario.save()
            
            return redirect('dispositivos')  
        except ValueError as e:
            
            error_message = str(e)
            return render(request, 'add_device.html', {'form': formulario, 'error_message': error_message})
    else:
        formulario = NewDevice()
    return render(request, 'add_device.html', {'form': formulario})


def edit_device(request, id):
    
    object = get_object_or_404(Device, id= id)  
    if request.method == 'POST':
        formulario = NewDevice(request.POST, instance=object)
        try:
            
            formulario.save()
            
            return redirect('dispositivos')  
        except ValueError as e:
            
            error_message = str(e)
            return render(request, 'edit_device.html', {'form': formulario, 'error_message': error_message})
    else:
        formulario = NewDevice(instance=object)  # Inicializa el formulario con la instancia del objeto
    return render(request, 'edit_device.html', {'form': formulario})
