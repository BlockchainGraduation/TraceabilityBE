from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .models import DetailDescription
from .serializers import DeitaiDescriptionSerializers

# Create your views here.


class DetailDescriptionView(ModelViewSet):
    queryset = DetailDescription.objects.all()
    serializer_class = DeitaiDescriptionSerializers

    def get_permissions(self):
        if (
            self.action == "partial_update"
            or self.action == "destroy"
            or self.action == "update"
        ):
            return [permissions.IsAuthenticated()]
        if self.action == "create":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
