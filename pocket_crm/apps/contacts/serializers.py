from rest_framework import serializers
from .models import Contact, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']

class ContactSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=Tag.objects.all(), source='tags', required=False
    )
    
    # As discussed, required in payload but values can be blank/null
    whatsapp = serializers.CharField(required=True, allow_blank=True, allow_null=True)
    telegram = serializers.CharField(required=True, allow_blank=True, allow_null=True)

    class Meta:
        model = Contact
        fields = [
            'id', 'name', 'email', 'phone', 'whatsapp', 'telegram', 
            'relationship', 'birthday', 'timezone', 'preferred_channel', 
            'status', 'tags', 'tag_ids', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_tag_ids(self, value):
        # Ensure that tags belong to the user
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            for tag in value:
                if tag.user != request.user:
                    raise serializers.ValidationError(f"Tag '{tag.name}' does not belong to you.")
        return value
