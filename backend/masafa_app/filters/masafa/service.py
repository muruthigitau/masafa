import django_filters as filters
from masafa_app.models.masafa.service import Service

class ServiceFilter(filters.FilterSet):
    id = filters.NumberFilter(label='ID')
    name = filters.CharFilter(lookup_expr='icontains', label='Name')
    price = filters.CharFilter(lookup_expr='icontains', label='Price')
    description = filters.CharFilter(lookup_expr='icontains', label='Description')

    class Meta:
        model = Service
        fields = ['id', 'name', 'price', 'description']

