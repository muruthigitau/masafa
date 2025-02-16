import django_filters as filters
from masafa_app.models.masafa.driver import Driver

class DriverFilter(filters.FilterSet):
    id = filters.NumberFilter(label='ID')
    first_name = filters.CharFilter(lookup_expr='icontains', label='First Name')
    last_name = filters.CharFilter(lookup_expr='icontains', label='Last Name')
    phone = filters.CharFilter(lookup_expr='icontains', label='Phone')

    class Meta:
        model = Driver
        fields = ['id', 'first_name', 'last_name', 'phone']

