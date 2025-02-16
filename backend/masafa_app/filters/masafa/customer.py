import django_filters as filters
from masafa_app.models.masafa.customer import Customer

class CustomerFilter(filters.FilterSet):
    id = filters.NumberFilter(label='ID')
    first_name = filters.CharFilter(lookup_expr='icontains', label='First Name')
    code = filters.CharFilter(lookup_expr='icontains', label='Code')
    last_name = filters.CharFilter(lookup_expr='icontains', label='Last Name')
    phone = filters.CharFilter(lookup_expr='icontains', label='Phone')
    email = filters.CharFilter(lookup_expr='icontains', label='Email')
    full_name = filters.CharFilter(lookup_expr='icontains', label='Full Name')

    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'code', 'last_name', 'phone', 'email', 'full_name']

