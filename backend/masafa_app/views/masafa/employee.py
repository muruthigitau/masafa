from rest_framework import viewsets
from core.views.template import GenericViewSet
from masafa_app.models.masafa.employee import Employee
from masafa_app.filters.masafa.employee import EmployeeFilter
from masafa_app.serializers.masafa.employee import EmployeeSerializer
from core.permissions import HasGroupPermission

class EmployeeViewSet(GenericViewSet):
    queryset = Employee.objects.all()
    filterset_class = EmployeeFilter
    permission_classes = [HasGroupPermission]
    serializer_class = EmployeeSerializer

