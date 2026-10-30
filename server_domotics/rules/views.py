from django.shortcuts import render, redirect, get_object_or_404
from .models import Rule
from devices.models import Device
from .forms import NewRule
from django.http import JsonResponse

# Create your views here.
def rules(request):
    rules_list = Rule.objects.all()
    return render(request, "rules.html", {"element_list": rules_list})

def add_rule(request):
    devices = Device.objects.all()
    if request.method == 'POST':
        formulario = NewRule(request.POST)
        
        try:
            
            formulario.save()
            
            return redirect('reglas')  
        except ValueError as e:
            
            error_message = str(e)
            return render(request, 'add_rule.html', {'form': formulario, 'error_message': error_message})
    else:
        formulario = NewRule()
    return render(request, 'add_rule.html', {'form': formulario})

def edit_rule(request, id):
    object = get_object_or_404(Rule, id= id)  
    if request.method == 'POST':
        formulario = NewRule(request.POST, instance=object)
        try:
            formulario.save()
            
            return redirect('reglas')  
        except ValueError as e:
            error_message = str(e)
            return render(request, 'edit_rule.html', {'form': formulario, 'error_message': error_message})
    else:
        formulario = NewRule(instance=object)  # Inicializa el formulario con la instancia del objeto
    return render(request, 'edit_rule.html', {'form': formulario})

def delete_rule(request, id):
    Rule.objects.get(id=id).delete()
    return JsonResponse({'cambio': True})



