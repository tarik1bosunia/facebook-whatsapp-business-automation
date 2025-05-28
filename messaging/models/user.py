from django.db import models


class SocialMediaUser(models.Model):
    name = models.CharField(max_length=100, blank=True)
    social_media_id = models.CharField(max_length=50, unique=True)
    avatar_url = models.URLField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.name} ({self.social_media_id})"