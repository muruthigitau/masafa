import django_filters as filters
from masafa_app.models.masafa.invoice import Invoice

class InvoiceFilter(filters.FilterSet):
    id = filters.NumberFilter(label='ID')
    type = filters.CharFilter(lookup_expr='icontains', label='Type')
    currency = filters.CharFilter(lookup_expr='icontains', label='Currency')
    status = filters.CharFilter(lookup_expr='icontains', label='Status')
    customer = filters.CharFilter(lookup_expr='icontains', label='Customer')
    total_amount = filters.CharFilter(lookup_expr='icontains', label='Total Amount')

    class Meta:
        model = Invoice
        fields = ['id', 'type', 'currency', 'status', 'customer', 'total_amount']

