from django.contrib import admin
from .models import Teacher, Subject, Classroom, Schedule

admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(Classroom)
admin.site.register(Schedule)