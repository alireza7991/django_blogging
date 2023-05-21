from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from content.models.content import Content
from content.models.rating import Rating


class RatingAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpass"
        )
        self.content = Content.objects.create(
            title="Test Content", text="Description for Test Content"
        )
        self.rating_data = {
            "content": self.content.id,
            "score": 3,
        }

    def test_create_rating(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/api/content/rate/", self.rating_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        rating = Rating.objects.get(content_id=response.data["content"])
        self.assertEqual(rating.score, self.rating_data["score"])

    def test_update_rating(self):
        self.client.force_authenticate(user=self.user)
        new_rating_data = {
            "content": self.content.id,
            "score": 5,
        }
        response = self.client.post("/api/content/rate/", new_rating_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        rating = Rating.objects.get(content_id=response.data["content"])
        self.assertEqual(new_rating_data["score"], rating.score)

    def test_out_of_range_create_rating(self):
        self.client.force_authenticate(user=self.user)
        bad_rating_data = {
            "content": self.content.id,
            "score": 6,
        }
        response = self.client.post("/api/content/rate/", bad_rating_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        bad_rating_data["score"] = -1
        response = self.client.post("/api/content/rate/", bad_rating_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
