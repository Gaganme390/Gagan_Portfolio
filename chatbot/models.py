from django.db import models


class ChatSession(models.Model):
    """Track chat sessions for analytics."""
    session_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    message_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Session {self.session_id[:8]}..."


class ChatMessage(models.Model):
    """Individual chat messages."""
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    is_user = models.BooleanField(default=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        role = "User" if self.is_user else "Bot"
        return f"{role}: {self.content[:50]}..."
