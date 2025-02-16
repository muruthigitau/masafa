from rest_framework import serializers
from core.serializers.template import RelationshipHandlerMixin
from masafa_app.models.masafa.item import Item

class ItemSerializer(RelationshipHandlerMixin, serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = '__all__'
