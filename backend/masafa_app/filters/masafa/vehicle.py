import django_filters as filters
from masafa_app.models.masafa.vehicle import Vehicle

class VehicleFilter(filters.FilterSet):
    id = filters.NumberFilter(label='ID')

    class Meta:
        model = Vehicle
        fields = ['id']

