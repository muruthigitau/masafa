import django_filters as filters
from masafa_app.models.masafa.payment import Payment

class PaymentFilter(filters.FilterSet):
    id = filters.NumberFilter(label='ID')
    date = filters.CharFilter(lookup_expr='icontains', label='Date')
    amount = filters.CharFilter(lookup_expr='icontains', label='Amount')
    source = filters.CharFilter(lookup_expr='icontains', label='Source')
    invoice = filters.CharFilter(lookup_expr='icontains', label='Invoice')
    transaction_no = filters.CharFilter(lookup_expr='icontains', label='Transaction No')
    currency = filters.CharFilter(lookup_expr='icontains', label='Currency')

    class Meta:
        model = Payment
        fields = ['id', 'date', 'amount', 'source', 'invoice', 'transaction_no', 'currency']

