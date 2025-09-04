"""DRF serializers act as DTOs between the outer HTTP layer and the use-cases."""
from rest_framework import serializers

class CreatePostSerializer(serializers.Serializer):
    # Input expected by the external API for creating a post
    username = serializers.CharField(max_length=150)
    title = serializers.CharField(max_length=200)
    content = serializers.CharField()

class UpdatePostSerializer(serializers.Serializer):
    # Partial fields allowed
    title = serializers.CharField(max_length=200, required=False)
    content = serializers.CharField(required=False)