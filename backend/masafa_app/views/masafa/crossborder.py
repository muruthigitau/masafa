from rest_framework import viewsets
from core.views.template import GenericViewSet
from masafa_app.models.masafa.crossborder import Crossborder
from masafa_app.filters.masafa.crossborder import CrossborderFilter
from masafa_app.serializers.masafa.crossborder import CrossborderSerializer
from core.permissions import HasGroupPermission

class CrossborderViewSet(GenericViewSet):
    queryset = Crossborder.objects.all()
    filterset_class = CrossborderFilter
    permission_classes = [HasGroupPermission]
    serializer_class = CrossborderSerializer

