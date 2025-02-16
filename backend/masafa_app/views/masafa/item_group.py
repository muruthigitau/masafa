from rest_framework import viewsets
from core.views.template import GenericViewSet
from masafa_app.models.masafa.item_group import ItemGroup
from masafa_app.filters.masafa.item_group import ItemGroupFilter
from masafa_app.serializers.masafa.item_group import ItemGroupSerializer
from core.permissions import HasGroupPermission

class ItemGroupViewSet(GenericViewSet):
    queryset = ItemGroup.objects.all()
    filterset_class = ItemGroupFilter
    permission_classes = [HasGroupPermission]
    serializer_class = ItemGroupSerializer

