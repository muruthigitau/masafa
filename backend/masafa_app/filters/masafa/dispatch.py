import django_filters as filters
from masafa_app.models.masafa.dispatch import Dispatch

class DispatchFilter(filters.FilterSet):
    id = filters.NumberFilter(label='ID')
    customer = filters.CharFilter(lookup_expr='icontains', label='Customer')
    receiver_name = filters.CharFilter(lookup_expr='icontains', label='Receiver Name')
    status = filters.CharFilter(lookup_expr='icontains', label='Status')
    receiver_phone = filters.CharFilter(lookup_expr='icontains', label='Receiver Phone')

    class Meta:
        model = Dispatch
        fields = ['id', 'customer', 'receiver_name', 'status', 'receiver_phone']

