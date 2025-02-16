import django_filters as filters
from masafa_app.models.masafa.item_group import ItemGroup

class ItemGroupFilter(filters.FilterSet):
    id = filters.NumberFilter(label='ID')

    class Meta:
        model = ItemGroup
        fields = ['id']

