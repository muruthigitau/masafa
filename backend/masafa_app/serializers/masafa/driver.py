from rest_framework import serializers
from core.serializers.template import RelationshipHandlerMixin
from masafa_app.models.masafa.driver import Driver

class DriverSerializer(RelationshipHandlerMixin, serializers.ModelSerializer):

    class Meta:
        model = Driver
        fields = '__all__'
