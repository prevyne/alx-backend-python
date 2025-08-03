from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    """
    Task 0: Creates a Notification when a new Message is saved.
    """
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            text=f"You have a new message from {instance.sender.username}."
        )

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Task 1: Before a message is updated, log its old content.
    """
    if instance.pk:  # Only run on updates, not creations
        try:
            original_message = Message.objects.get(pk=instance.pk)
            if original_message.content != instance.content:
                MessageHistory.objects.create(
                    message=original_message,
                    old_content=original_message.content
                )
                instance.edited = True
        except Message.DoesNotExist:
            pass # Message is being created, do nothing.

@receiver(post_delete, sender=User)
def delete_user_data(sender, instance, **kwargs):
    """
    Task 2: Confirms cleanup after a user is deleted.
    Note: `on_delete=models.CASCADE` in the models already handles the deletion.
    This signal is for demonstration or for adding extra logic like logging.
    """
    print(f"User {instance.username} has been deleted. "
          f"Their associated data was removed via CASCADE settings.")