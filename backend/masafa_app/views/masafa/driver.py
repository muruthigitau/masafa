from rest_framework import viewsets
from core.views.template import GenericViewSet
from masafa_app.models.masafa.driver import Driver
from masafa_app.filters.masafa.driver import DriverFilter
from masafa_app.serializers.masafa.driver import DriverSerializer
from core.permissions import HasGroupPermission

# from apps.masafa.masafa.masafa.doctype.driver.driver import Driver as CustomDriver

class DriverViewSet(GenericViewSet):
    queryset = Driver.objects.all()
    filterset_class = DriverFilter
    permission_classes = [HasGroupPermission]
    serializer_class = DriverSerializer

