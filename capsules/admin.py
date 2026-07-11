from django.contrib import admin

from .models import Capsule

@admin.register(Capsule)
class CapsuleAdmin(admin.ModelAdmin):
    list_display = ("title", "recipient_email", "unlock_at", "status")
    list_filter = ("status", )
    search_fields = ("title", "recipient_email")
