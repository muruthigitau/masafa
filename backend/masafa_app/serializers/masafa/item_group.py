from rest_framework import serializers
from core.serializers.template import RelationshipHandlerMixin
from masafa_app.models.masafa.item_group import ItemGroup

class ItemGroupSerializer(RelationshipHandlerMixin, serializers.ModelSerializer):

    class Meta:
        model = ItemGroup
        fields = '__all__'
