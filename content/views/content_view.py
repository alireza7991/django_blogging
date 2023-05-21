from rest_framework import generics, permissions
from django.db import models
from content.models.content import Content
from content.models.rating import Rating
from content.serializers.content_serializer import ContentSerializer
from content.serializers.rating_serializer import ContentRatingSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ContentListAPIView(generics.ListAPIView):
    queryset = Content.objects.annotate(
        num_ratings=models.Count("rating"), avg_rating=models.Avg("rating__score")
    )

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        for content in queryset:
            rating = Rating.objects.filter(content=content, user=user).first()
            if rating:
                content.user_rating = rating
        return queryset

    serializer_class = ContentSerializer
