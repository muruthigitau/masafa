from rest_framework import serializers
from core.serializers.template import RelationshipHandlerMixin
from masafa_app.models.masafa.vehicle import Vehicle

class VehicleSerializer(RelationshipHandlerMixin, serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        fields = '__all__'
