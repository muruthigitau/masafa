import django_filters as filters
from masafa_app.models.masafa.supplier import Supplier

class SupplierFilter(filters.FilterSet):
    id = filters.NumberFilter(label='ID')
    name = filters.CharFilter(lookup_expr='icontains', label='Name')
    location = filters.CharFilter(lookup_expr='icontains', label='Location')
    phone = filters.CharFilter(lookup_expr='icontains', label='Phone')

    class Meta:
        model = Supplier
        fields = ['id', 'name', 'location', 'phone']

