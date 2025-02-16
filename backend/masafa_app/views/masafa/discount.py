from rest_framework import viewsets
from core.views.template import GenericViewSet
from masafa_app.models.masafa.discount import Discount
from masafa_app.filters.masafa.discount import DiscountFilter
from masafa_app.serializers.masafa.discount import DiscountSerializer
from core.permissions import HasGroupPermission

class DiscountViewSet(GenericViewSet):
    queryset = Discount.objects.all()
    filterset_class = DiscountFilter
    permission_classes = [HasGroupPermission]
    serializer_class = DiscountSerializer

