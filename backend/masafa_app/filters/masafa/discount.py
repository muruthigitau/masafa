import django_filters as filters
from masafa_app.models.masafa.discount import Discount

class DiscountFilter(filters.FilterSet):
    id = filters.NumberFilter(label='ID')

    class Meta:
        model = Discount
        fields = ['id']

