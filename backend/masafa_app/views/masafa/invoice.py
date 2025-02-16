from rest_framework import viewsets
from core.views.template import GenericViewSet
from masafa_app.models.masafa.invoice import Invoice
from masafa_app.filters.masafa.invoice import InvoiceFilter
from masafa_app.serializers.masafa.invoice import InvoiceSerializer
from core.permissions import HasGroupPermission

# from apps.masafa.masafa.masafa.doctype.invoice.invoice import Invoice as CustomInvoice

class InvoiceViewSet(GenericViewSet):
    queryset = Invoice.objects.all()
    filterset_class = InvoiceFilter
    permission_classes = [HasGroupPermission]
    serializer_class = InvoiceSerializer

