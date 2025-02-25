import django_filters as filters
from masafa_app.models.masafa.item import Item

class ItemFilter(filters.FilterSet):
    id = filters.NumberFilter(label='ID')
    item_group = filters.CharFilter(lookup_expr='icontains', label='Item Group')
    name = filters.CharFilter(lookup_expr='icontains', label='Name')
    weight = filters.CharFilter(lookup_expr='icontains', label='Weight')
    packaging_type = filters.CharFilter(lookup_expr='icontains', label='Packaging Type')
    type = filters.CharFilter(lookup_expr='icontains', label='Type')
    customer = filters.CharFilter(lookup_expr='icontains', label='Customer')
    status = filters.CharFilter(lookup_expr='icontains', label='Status')
    item_condition = filters.CharFilter(lookup_expr='icontains', label='Item Condition')

    class Meta:
        model = Item
        fields = ['id', 'item_group', 'name', 'weight', 'packaging_type', 'type', 'customer', 'status', 'item_condition']

