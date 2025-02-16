from rest_framework import serializers
from core.serializers.template import RelationshipHandlerMixin
from masafa_app.models.masafa.crossborder import Crossborder

class CrossborderSerializer(RelationshipHandlerMixin, serializers.ModelSerializer):

    class Meta:
        model = Crossborder
        fields = '__all__'
