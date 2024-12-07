from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import Thread, Message, CustomUser, ThreadParticipant
from uuid import uuid4


class ChatAPITestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

        # Create users
        self.user1 = CustomUser.objects.create_user(
            email="user1@example.com", password="password1", name="User One"
        )
        self.user2 = CustomUser.objects.create_user(
            email="user2@example.com", password="password2", name="User Two"
        )

        # Authenticate user1
        self.client.force_authenticate(user=self.user1)

        # Create a thread
        self.thread = Thread.objects.create(
            entity_type="chat",
            entity_id=uuid4(),
            title="Test Thread",
            created_by=self.user1,
        )

        # Create a message
        self.message = Message.objects.create(
            thread=self.thread,
            user=self.user1,
            content="Hello, World!",
            created_by=self.user1,
        )

        # Add a participant
        self.participant = ThreadParticipant.objects.create(
            thread=self.thread, user=self.user1, created_by=self.user1
        )

    def test_get_thread_messages(self):
        url = reverse("thread-messages", kwargs={"thread_id": self.thread.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["content"], "Hello, World!")

    def test_post_thread_message(self):
        url = reverse("thread-messages", kwargs={"thread_id": self.thread.id})
        data = {"user": str(self.user1.id), "content": "New Message"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["content"], "New Message")

    def test_get_thread_participants(self):
        url = reverse("thread-participants", kwargs={"thread_id": self.thread.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["user_name"], "User One")

    def test_post_thread_participant(self):
        url = reverse("thread-participants", kwargs={"thread_id": self.thread.id})
        data = {"user": str(self.user2.id)}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["user_id"], str(self.user2.id))

    def test_post_existing_thread_participant(self):
        url = reverse("thread-participants", kwargs={"thread_id": self.thread.id})
        data = {"user": str(self.user1.id)}  # user1 is already a participant
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user_id"], str(self.user1.id))

    def test_get_nonexistent_thread_messages(self):
        url = reverse("thread-messages", kwargs={"thread_id": uuid4()})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_message_to_nonexistent_thread(self):
        url = reverse("thread-messages", kwargs={"thread_id": uuid4()})
        data = {"user": str(self.user1.id), "content": "Message"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_participant_to_nonexistent_thread(self):
        url = reverse("thread-participants", kwargs={"thread_id": uuid4()})
        data = {"user": str(self.user2.id)}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_access(self):
        self.client.force_authenticate(user=None)  # Unauthenticate

        url = reverse("thread-messages", kwargs={"thread_id": self.thread.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
