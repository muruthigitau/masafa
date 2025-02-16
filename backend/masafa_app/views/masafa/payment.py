from rest_framework import viewsets
from core.views.template import GenericViewSet
from masafa_app.models.masafa.payment import Payment
from masafa_app.filters.masafa.payment import PaymentFilter
from masafa_app.serializers.masafa.payment import PaymentSerializer
from core.permissions import HasGroupPermission

class PaymentViewSet(GenericViewSet):
    queryset = Payment.objects.all()
    filterset_class = PaymentFilter
    permission_classes = [HasGroupPermission]
    serializer_class = PaymentSerializer

