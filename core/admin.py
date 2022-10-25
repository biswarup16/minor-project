from django.contrib import admin
from . models import *

# Register your models here.

admin.site.register(Profile)

admin.site.register(Prospectus)

admin.site.register(AdmissionForm)

admin.site.register(AdmissionDocument)

admin.site.register(UploadFile)



@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ['name']
    def has_add_permission(self, request):
        if(self.model.objects.count() == 0):
            return True
        else:
            return False