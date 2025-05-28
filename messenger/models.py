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



class Conversation(models.Model):
    CHANNEL_CHOICES = [
        ('facebook', 'Facebook'),
        ('whatsapp', 'WhatsApp'),
    ]
    user = models.ForeignKey(SocialMediaUser, on_delete=models.CASCADE, related_name='conversations')
    channel = models.CharField(max_length=10, choices=CHANNEL_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
    
    def last_message(self):
        return self.messages.order_by('-created_at').first()

    def unread_count(self):
        return self.messages.filter(sender='customer', is_read=False).count()
    
    def __str__(self):
        return f"Conversation with {self.user.name} ({self.user.social_media_id})"
    

class ChatMessage(models.Model):
    SENDER_CHOICES = (
        ('customer', 'Customer'),
        ('business', 'Business'),
        ('ai', 'AI'),
    )

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES, default='business')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.conversation}: {self.sender} - {self.message[:50]}"
