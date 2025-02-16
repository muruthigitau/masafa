import django_filters as filters
from masafa_app.models.masafa.crossborder import Crossborder

class CrossborderFilter(filters.FilterSet):
    id = filters.NumberFilter(label='ID')
    status = filters.CharFilter(lookup_expr='icontains', label='Status')
    loading_point = filters.CharFilter(lookup_expr='icontains', label='Loading Point')
    destination = filters.CharFilter(lookup_expr='icontains', label='Destination')

    class Meta:
        model = Crossborder
        fields = ['id', 'status', 'loading_point', 'destination']

