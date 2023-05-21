from rest_framework import serializers
from content.models.content import Content
from content.models.rating import Rating
from content.serializers.rating_serializer import ContentRatingSerializer


class ContentSerializer(serializers.ModelSerializer):
    num_ratings = serializers.IntegerField(read_only=True)
    avg_rating = serializers.FloatField(read_only=True)
    user_rating = ContentRatingSerializer(read_only=True)

    class Meta:
        model = Content
        fields = ("id", "title", "text", "num_ratings", "avg_rating", "user_rating")

    def create(self, validated_data):
        content = Content.objects.create(**validated_data)
        return content

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.text = validated_data.get("text", instance.text)
        instance.save()
        return instance
