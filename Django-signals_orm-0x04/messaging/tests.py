from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class SignalsTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')

    def test_notification_created_on_new_message(self):
        """
        Test that a notification is created automatically when a message is sent.
        """
        # Check that no notifications exist initially for user2
        self.assertEqual(Notification.objects.filter(user=self.user2).count(), 0)

        # User1 sends a message to User2
        Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Hello, User2!"
        )

        # Check that a notification has been created for user2
        self.assertEqual(Notification.objects.filter(user=self.user2).count(), 1)
        notification = Notification.objects.get(user=self.user2)
        self.assertEqual(notification.text, f"You have a new message from {self.user1.username}.")