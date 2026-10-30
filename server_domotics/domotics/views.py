from django.http import JsonResponse
from django.shortcuts import render
from .models import Event

# Create your views here.

def home(request):
    return render(request, "home.html", {})

def events(request):
    messages = "YES"
    all_events = Event.objects.all()
    not_read_events = Event.objects.filter(read=False)
    events_size = len(not_read_events)
    if events_size == 0:
        messages = "NO"
    return render(request, "events.html", {"all_events": all_events, "not_read_events": not_read_events, "size_events": events_size, "messages": messages})

def event_read(request, id):
    event = Event.objects.get(id=id)
    event.read = True
    event.save()
    return JsonResponse({'cambio': True})
