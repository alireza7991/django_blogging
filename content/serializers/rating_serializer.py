from rest_framework import serializers
from content.models.content import Content
from content.models.rating import Rating


class ContentRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ("score", "created_at", "updated_at")


class CreateRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ("content", "score")
