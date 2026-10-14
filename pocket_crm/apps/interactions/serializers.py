from rest_framework import serializers
from .models import Interaction

class InteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interaction
        fields = ['id', 'channel', 'occurred_at', 'summary', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
