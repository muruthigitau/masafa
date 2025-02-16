from rest_framework import serializers
from core.serializers.template import RelationshipHandlerMixin
from masafa_app.models.masafa.supplier import Supplier

class SupplierSerializer(RelationshipHandlerMixin, serializers.ModelSerializer):

    class Meta:
        model = Supplier
        fields = '__all__'
