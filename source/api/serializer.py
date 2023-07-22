from rest_framework import serializers
from .models import Client, Deal, Gem

class GemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gem
        fields = '__all__'

class DealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deal
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    deals = DealSerializer(many=True)

    class Meta:
        model = Client
        fields = ('username', 'deals')


