from django.contrib import admin

# Register your models here.
from web import models

admin.site.register(models.Project)
admin.site.register(models.Host)
admin.site.register(models.UserInfo)
admin.site.register(models.LogInfo)
