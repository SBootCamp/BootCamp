from django.contrib import admin

from .models import Mentor, Student, ScheduleS, StudentScheduleS

admin.site.register(Mentor)
admin.site.register(Student)
admin.site.register(ScheduleS)
admin.site.register(StudentScheduleS)

