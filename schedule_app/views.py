from django.shortcuts import render
from .models import Schedule

def schedule_list(request):
    schedules = Schedule.objects.all()
    return render(request, 'schedule_app/schedule_list.html', {'schedules': schedules})
