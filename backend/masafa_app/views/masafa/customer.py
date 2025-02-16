from rest_framework import viewsets
from core.views.template import GenericViewSet
from masafa_app.models.masafa.customer import Customer
from masafa_app.filters.masafa.customer import CustomerFilter
from masafa_app.serializers.masafa.customer import CustomerSerializer
from core.permissions import HasGroupPermission

class CustomerViewSet(GenericViewSet):
    queryset = Customer.objects.all()
    filterset_class = CustomerFilter
    permission_classes = [HasGroupPermission]
    serializer_class = CustomerSerializer

