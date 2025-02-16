import django_filters as filters
from masafa_app.models.masafa.employee import Employee

class EmployeeFilter(filters.FilterSet):
    id = filters.NumberFilter(label='ID')

    class Meta:
        model = Employee
        fields = ['id']

