from django.contrib import admin
from content.models.content import Content
from content.models.rating import Rating

admin.site.register(Content)
admin.site.register(Rating)
