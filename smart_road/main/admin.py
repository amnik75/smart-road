from django.contrib import admin

# Register your models here.

from .models import Pass,Camera,Road

admin.site.register(Pass)
admin.site.register(Camera)
admin.site.register(Road)
