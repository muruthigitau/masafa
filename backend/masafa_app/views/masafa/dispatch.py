from rest_framework import viewsets
from core.views.template import GenericViewSet
from masafa_app.models.masafa.dispatch import Dispatch
from masafa_app.filters.masafa.dispatch import DispatchFilter
from masafa_app.serializers.masafa.dispatch import DispatchSerializer
from core.permissions import HasGroupPermission

# from apps.masafa.masafa.masafa.doctype.dispatch.dispatch import Dispatch as CustomDispatch

class DispatchViewSet(GenericViewSet):
    queryset = Dispatch.objects.all()
    filterset_class = DispatchFilter
    permission_classes = [HasGroupPermission]
    serializer_class = DispatchSerializer

