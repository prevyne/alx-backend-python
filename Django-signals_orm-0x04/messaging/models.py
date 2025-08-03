from django.db import models
from django.contrib.auth.models import User

# --- Custom Manager (Task 4) ---
class UnreadMessagesManager(models.Manager):
    """Custom manager to return only unread messages."""
    def get_queryset(self):
        return super().get_queryset().filter(is_read=False)

# --- Message Model (Tasks 0, 1, 3, 4) ---
class Message(models.Model):
    """Represents a message, with support for threading and read status."""
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    parent_message = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    edited = models.BooleanField(default=False)

    # Managers
    objects = models.Manager()  # The default manager
    unread = UnreadMessagesManager()  # The custom unread manager

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username}"

# --- Notification Model (Task 0) ---
class Notification(models.Model):
    """Stores notifications for users, triggered by new messages."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}"

# --- Message History Model (Task 1 & Checker Fix) ---
class MessageHistory(models.Model):
    """Logs the history of edits for a message."""
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    edited_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-edited_at']
        verbose_name_plural = "Message histories"

    def __str__(self):
        editor = self.edited_by.username if self.edited_by else "an unknown user"
        return f"Edit for message {self.message.id} by {editor}"