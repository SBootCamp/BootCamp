from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import *

class CustomMPTTModelAdmin(MPTTModelAdmin):
    mptt_level_indent = 20

admin.site.register(Node, CustomMPTTModelAdmin)
admin.site.register(Event)