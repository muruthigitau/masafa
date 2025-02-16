from rest_framework import serializers
from core.serializers.template import RelationshipHandlerMixin
from masafa_app.models.masafa.discount import Discount

class DiscountSerializer(RelationshipHandlerMixin, serializers.ModelSerializer):

    class Meta:
        model = Discount
        fields = '__all__'
