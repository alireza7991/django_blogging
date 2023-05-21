from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from django.db import models
from content.models.content import Content
from content.models.rating import Rating
from content.serializers.content_serializer import ContentSerializer
from content.serializers.rating_serializer import CreateRatingSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class RatingCreateAPIView(generics.CreateAPIView):
    serializer_class = CreateRatingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        content_id = serializer.validated_data.get("content").id
        user = request.user
        existing_rating = Rating.objects.filter(
            content_id=content_id, user=user
        ).first()
        if existing_rating:
            existing_rating.score = serializer.validated_data.get("score")
            existing_rating.save()
            return Response(
                self.get_serializer(existing_rating).data, status=status.HTTP_200_OK
            )
        else:
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
