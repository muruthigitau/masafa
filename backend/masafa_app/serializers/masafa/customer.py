from rest_framework import serializers
from core.serializers.template import RelationshipHandlerMixin
from masafa_app.models.masafa.customer import Customer

class CustomerSerializer(RelationshipHandlerMixin, serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'
