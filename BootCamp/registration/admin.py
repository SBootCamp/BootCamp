from django.contrib import admin

from .models import Mentor, Student, ScheduleS
from .models import Profile, Achievement, Flow

admin.site.register(Profile)
admin.site.register(Achievement)
admin.site.register(Flow)
admin.site.register(Mentor)
admin.site.register(Student)
admin.site.register(ScheduleS)
# admin.site.register(StudentScheduleS)

