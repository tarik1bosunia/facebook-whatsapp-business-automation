from django.db import models

from messaging.models.conversation import Conversation


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