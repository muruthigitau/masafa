import django_filters as filters
from masafa_app.models.masafa.paymentdetails import Paymentdetails

class PaymentdetailsFilter(filters.FilterSet):
    id = filters.NumberFilter(label='ID')
    name = filters.CharFilter(lookup_expr='icontains', label='Name')
    account_name = filters.CharFilter(lookup_expr='icontains', label='Account Name')
    account_number = filters.CharFilter(lookup_expr='icontains', label='Account Number')
    currency = filters.CharFilter(lookup_expr='icontains', label='Currency')
    branch = filters.CharFilter(lookup_expr='icontains', label='Branch')

    class Meta:
        model = Paymentdetails
        fields = ['id', 'name', 'account_name', 'account_number', 'currency', 'branch']

