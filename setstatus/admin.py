from django.contrib import admin
from setstatus.models import SetStatus

class SetStatusAdminInline(admin.StackedInline):
    model = SetStatus
    exclude = ('modified_by',)

    def save_model(self, request, obj, form, change):
        """
        Save the current user as the modifying user.

        """
        obj.modified_by = request.user
        obj.save()

class SetStatusAdmin(admin.Model):
    list_display = ["status", "start_at", "end_at", "active", "content_object"]
    exclude = ('modified_by',)

admin.site.register(SetStatus, SetStatusAdmin)
