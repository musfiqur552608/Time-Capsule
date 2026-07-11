from django.utils import timezone
from rest_framework import serializers

from .models import Capsule


class CapsuleSerializer(serializers.ModelSerializer):
    message = serializers.SerializerMethodField()

    class Meta:
        model = Capsule
        fields = [
            "id", "recipient_email", "title", "message",
            "unlock_at", "status", "created_at", "delivered_at",
        ]
    
    def get_message(self, obj):
        if obj.status == Capsule.Status.SEALED: return "Sealed until " + obj.unlock_at.strftime("%Y-%m-%d %H:%M UTC")
        return obj.message

class CapsuleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Capsule
        fields = ["id", "recipient_email", "title", "message", "unlock_at"]

    def validate_unlock_at(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("Unlock time must be in the future")
        return value
        