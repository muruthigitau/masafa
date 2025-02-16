from rest_framework import viewsets
from core.views.template import GenericViewSet
from masafa_app.models.masafa.item import Item
from masafa_app.filters.masafa.item import ItemFilter
from masafa_app.serializers.masafa.item import ItemSerializer
from core.permissions import HasGroupPermission

class ItemViewSet(GenericViewSet):
    queryset = Item.objects.all()
    filterset_class = ItemFilter
    permission_classes = [HasGroupPermission]
    serializer_class = ItemSerializer

