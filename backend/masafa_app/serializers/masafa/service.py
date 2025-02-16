from rest_framework import serializers
from core.serializers.template import RelationshipHandlerMixin
from masafa_app.models.masafa.service import Service

class ServiceSerializer(RelationshipHandlerMixin, serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = '__all__'
