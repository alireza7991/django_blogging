from django.urls import path
from content.views.content_view import ContentListAPIView
from content.views.rating_view import RatingCreateAPIView

urlpatterns = [
    path("list/", ContentListAPIView.as_view(), name="content_list"),
    path("rate/", RatingCreateAPIView.as_view(), name="rate_content"),
]
