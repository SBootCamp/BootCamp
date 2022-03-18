from django.contrib import admin

from .models import ScheduleS
from .models import Profile, Achievement, Flow

admin.site.register(Profile)
admin.site.register(Achievement)
admin.site.register(Flow)
admin.site.register(ScheduleS)

