from rest_framework import serializers
from crimes.models import Crime


class CrimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crime
        fields = '__all__'
