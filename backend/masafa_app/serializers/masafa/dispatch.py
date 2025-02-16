from rest_framework import serializers
from core.serializers.template import RelationshipHandlerMixin
from masafa_app.models.masafa.dispatch import Dispatch

class DispatchSerializer(RelationshipHandlerMixin, serializers.ModelSerializer):

    class Meta:
        model = Dispatch
        fields = '__all__'
