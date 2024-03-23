from rest_framework import serializers
from .models import RegisterData

class RegSerializer(serializers.ModelSerializer):
    created_by=serializers.CharField(required=False)
    class Meta:
        model = RegisterData
        fields  = '__all__'
        