from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'contact', 'touchpoint', 'body', 'status', 'purpose', 'tone', 'length', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class MessageGenerateSerializer(serializers.Serializer):
    contact_id = serializers.IntegerField()
    purpose = serializers.CharField(required=False, allow_blank=True)
    tone = serializers.CharField(required=False, allow_blank=True)
    length = serializers.CharField(required=False, allow_blank=True)
    custom_instruction = serializers.CharField(required=False, allow_blank=True)
