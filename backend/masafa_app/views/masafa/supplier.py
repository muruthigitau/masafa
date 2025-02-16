from rest_framework import viewsets
from core.views.template import GenericViewSet
from masafa_app.models.masafa.supplier import Supplier
from masafa_app.filters.masafa.supplier import SupplierFilter
from masafa_app.serializers.masafa.supplier import SupplierSerializer
from core.permissions import HasGroupPermission

class SupplierViewSet(GenericViewSet):
    queryset = Supplier.objects.all()
    filterset_class = SupplierFilter
    permission_classes = [HasGroupPermission]
    serializer_class = SupplierSerializer

