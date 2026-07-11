from rest_framework import viewsets

from .models import Capsule
from .serializers import CapsuleSerializer, CapsuleCreateSerializer


class CapsuleViewSet(viewsets.ModelViewSet):
    queryset = Capsule.objects.all()
    http_method_names = ["get", "post", "delete"]

    def get_serializer_class(self):
        if self.action == "create":
            return CapsuleCreateSerializer
        return CapsuleSerializer