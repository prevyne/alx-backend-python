from django.db import models

class UnreadMessagesManager(models.Manager):
    """Custom manager for Message model."""
    
    def get_queryset(self):
        """Filters for messages that are not read."""
        return super().get_queryset().filter(is_read=False)

    def unread_for_user(self, user):
        """Returns a queryset of unread messages for a specific user."""
        return self.get_queryset().filter(receiver=user)