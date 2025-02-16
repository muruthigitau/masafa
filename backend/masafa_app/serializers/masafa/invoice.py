from rest_framework import serializers
from core.serializers.template import RelationshipHandlerMixin
from masafa_app.models.masafa.invoice import Invoice

class InvoiceSerializer(RelationshipHandlerMixin, serializers.ModelSerializer):

    class Meta:
        model = Invoice
        fields = '__all__'
