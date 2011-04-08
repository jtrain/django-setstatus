from django.contrib import admin
from django.contrib.contenttypes.generic import GenericStackedInline
from setstatus.models import SetStatus
from django.forms.models import ModelForm

class SetStatusAdminInline(GenericStackedInline):
    model = SetStatus
    extra = 1

class SetStatusAdmin(admin.ModelAdmin):
    list_display = ["status", "start_at", "end_at", "active", "content_object"]

admin.site.register(SetStatus, SetStatusAdmin)
