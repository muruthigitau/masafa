from rest_framework import viewsets
from core.views.template import GenericViewSet
from masafa_app.models.masafa.service import Service
from masafa_app.filters.masafa.service import ServiceFilter
from masafa_app.serializers.masafa.service import ServiceSerializer
from core.permissions import HasGroupPermission

class ServiceViewSet(GenericViewSet):
    queryset = Service.objects.all()
    filterset_class = ServiceFilter
    permission_classes = [HasGroupPermission]
    serializer_class = ServiceSerializer

