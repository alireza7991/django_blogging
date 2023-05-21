from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from content.models.content import Content
from content.models.rating import Rating
from content.serializers.content_serializer import ContentSerializer


class SimpleListTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpass"
        )
        self.content1 = Content.objects.create(
            title="Test Content 1", text="Desc for Test Content 1"
        )
        self.content2 = Content.objects.create(
            title="Test Content 2", text="Desc for Test Content 2"
        )
        self.rating1 = Rating.objects.create(
            user=self.user, content=self.content1, score=3
        )

    def test_content_list_with_user_rating(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/content/list/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content_data = response.data
        self.assertEqual(len(content_data), 2)
        serializer = ContentSerializer([self.content1, self.content2], many=True)
        for field in serializer.data[0].items():
            self.assertIn(field, content_data[0].items())
        for field in serializer.data[1].items():
            self.assertIn(field, content_data[1].items())
        self.assertIn("user_rating", content_data[0].keys())
        self.assertNotIn("user_rating", content_data[1].keys())


class ScoreCalculationTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="testuser1", email="testuser1@example.com", password="testpass1"
        )
        self.user2 = User.objects.create_user(
            username="testuser2", email="testuser2@example.com", password="testpass2"
        )
        self.user3 = User.objects.create_user(
            username="testuser3", email="testuser3@example.com", password="testpass3"
        )
        self.content1 = Content.objects.create(
            title="Test Content 1", text="Description for Test Content 1"
        )
        self.content2 = Content.objects.create(
            title="Test Content 2", text="Description for Test Content 2"
        )
        self.rating1 = Rating.objects.create(
            user=self.user1, content=self.content1, score=3
        )
        self.rating2 = Rating.objects.create(
            user=self.user2, content=self.content1, score=4
        )
        self.rating3 = Rating.objects.create(
            user=self.user1, content=self.content2, score=5
        )
        self.rating4 = Rating.objects.create(
            user=self.user2, content=self.content2, score=2
        )
        self.rating5 = Rating.objects.create(
            user=self.user3, content=self.content2, score=3
        )

    def test_content_score_calculation(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get("/api/content/list/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content_data = response.data
        content1_expected_score = (3 + 4) / 2
        content2_expected_score = (5 + 2 + 3) / 3
        self.assertAlmostEqual(
            content_data[0]["avg_rating"], content1_expected_score, places=2
        )
        self.assertAlmostEqual(
            content_data[1]["avg_rating"], content2_expected_score, places=2
        )
