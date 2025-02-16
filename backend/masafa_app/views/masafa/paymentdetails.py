from rest_framework import viewsets
from core.views.template import GenericViewSet
from masafa_app.models.masafa.paymentdetails import Paymentdetails
from masafa_app.filters.masafa.paymentdetails import PaymentdetailsFilter
from masafa_app.serializers.masafa.paymentdetails import PaymentdetailsSerializer
from core.permissions import HasGroupPermission

class PaymentdetailsViewSet(GenericViewSet):
    queryset = Paymentdetails.objects.all()
    filterset_class = PaymentdetailsFilter
    permission_classes = [HasGroupPermission]
    serializer_class = PaymentdetailsSerializer

