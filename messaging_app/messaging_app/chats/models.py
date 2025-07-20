import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Uses a UUID for the primary key.
    """
    # Override the default id to use UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # The 'role' enum as specified in the database schema
    ROLE_CHOICES = (
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    )
    
    # Additional fields
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')

    # The AbstractUser already includes:
    # username, first_name, last_name, email, password, etc.
    # We will use the built-in email field and password hashing.

    def __str__(self):
        return self.username

class Conversation(models.Model):
    """
    Represents a conversation between two or more users.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"

class Message(models.Model):
    """
    Represents a single message within a conversation.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sent_at'] # Order messages by when they were sent

    def __str__(self):
        return f"Message from {self.sender.username} at {self.sent_at}"