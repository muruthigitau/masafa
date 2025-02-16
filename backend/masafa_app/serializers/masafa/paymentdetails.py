from rest_framework import serializers
from core.serializers.template import RelationshipHandlerMixin
from masafa_app.models.masafa.paymentdetails import Paymentdetails

class PaymentdetailsSerializer(RelationshipHandlerMixin, serializers.ModelSerializer):

    class Meta:
        model = Paymentdetails
        fields = '__all__'
