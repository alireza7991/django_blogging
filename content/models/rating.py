from django.db import models
from django.contrib.auth.models import User
from content.models.content import Content
from django.core import validators


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    score = models.IntegerField(
        validators=[validators.MinValueValidator(0), validators.MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "content")

    def __str__(self):
        return f"{self.user} rated {self.content} with {self.score} points"
