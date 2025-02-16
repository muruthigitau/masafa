from rest_framework import serializers
from core.serializers.template import RelationshipHandlerMixin
from masafa_app.models.masafa.employee import Employee

class EmployeeSerializer(RelationshipHandlerMixin, serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = '__all__'
