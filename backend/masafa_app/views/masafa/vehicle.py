from rest_framework import viewsets
from core.views.template import GenericViewSet
from masafa_app.models.masafa.vehicle import Vehicle
from masafa_app.filters.masafa.vehicle import VehicleFilter
from masafa_app.serializers.masafa.vehicle import VehicleSerializer
from core.permissions import HasGroupPermission

# from apps.masafa.masafa.masafa.doctype.vehicle.vehicle import Vehicle as CustomVehicle

class VehicleViewSet(GenericViewSet):
    queryset = Vehicle.objects.all()
    filterset_class = VehicleFilter
    permission_classes = [HasGroupPermission]
    serializer_class = VehicleSerializer

