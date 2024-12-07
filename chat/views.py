from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from users.models import CustomUser
from .models import Thread, Message, ThreadParticipant
from .serializers import (
    CreateMessageSerializer,
    CreateParticipantSerializer,
    ParticipantSerializer,
    ThreadMessageSerializer,
    ThreadSerializer,
    MessageSerializer,
    ThreadParticipantSerializer,
)


class ThreadListCreateAPIView(APIView):
    """
    List all threads or create a new thread.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(f"{request.query_params=}")
        if request.query_params:
            entity_id = request.query_params.get("entity_id")
            entity_type = request.query_params.get("entity_type")

            if not entity_id or not entity_type:
                return Response(
                    {"error": "Both 'entity_id' and 'entity_type' are required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Filter threads based on entity_id and entity_type
            threads = Thread.objects.filter(
                entity_id=entity_id, entity_type=entity_type
            )

            # Serialize the threads
            serializer = ThreadSerializer(threads, many=True)

            return Response(serializer.data)
        threads = Thread.objects.filter(is_deleted=False)  # Filter by is_deleted=False
        serializer = ThreadSerializer(threads, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ThreadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)  # Automatically set created_by
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ThreadRetrieveUpdateDestroyAPIView(APIView):
    """
    Retrieve, update or delete a specific thread.
    """

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Thread.objects.get(
                pk=pk, is_deleted=False
            )  # Check if the thread is not deleted
        except Thread.DoesNotExist:
            return None

    def get(self, request, pk):
        thread = self.get_object(pk)
        if thread is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ThreadSerializer(thread)
        return Response(serializer.data)

    def put(self, request, pk):
        thread = self.get_object(pk)
        if thread is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ThreadSerializer(thread, data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)  # Automatically set created_by
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        thread = self.get_object(pk)
        if thread is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        thread.is_deleted = True
        thread.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MessageListCreateAPIView(APIView):
    """
    List all messages or create a new message.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        messages = Message.objects.filter(
            is_deleted=False
        )  # Filter by is_deleted=False
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)  # Automatically set created_by
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageRetrieveUpdateDestroyAPIView(APIView):
    """
    Retrieve, update, or delete a specific message.
    """

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Message.objects.get(
                pk=pk, is_deleted=False
            )  # Check if the message is not deleted
        except Message.DoesNotExist:
            return None

    def get(self, request, pk):
        message = self.get_object(pk)
        if message is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = MessageSerializer(message)
        return Response(serializer.data)

    def put(self, request, pk):
        message = self.get_object(pk)
        if message is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = MessageSerializer(message, data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)  # Automatically set created_by
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        message = self.get_object(pk)
        if message is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ThreadParticipantListCreateAPIView(APIView):
    """
    List all participants or add a new participant.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):

        participants = ThreadParticipant.objects.filter(
            is_deleted=False
        )  # Filter by is_deleted=False
        serializer = ThreadParticipantSerializer(participants, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ThreadParticipantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)  # Automatically set created_by
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ThreadParticipantRetrieveUpdateDestroyAPIView(APIView):
    """
    Retrieve, update, or delete a specific participant.
    """

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return ThreadParticipant.objects.get(
                pk=pk, is_deleted=False
            )  # Check if the participant is not deleted
        except ThreadParticipant.DoesNotExist:
            return None

    def get(self, request, pk):
        participant = self.get_object(pk)
        if participant is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ThreadParticipantSerializer(participant)
        return Response(serializer.data)

    def put(self, request, pk):
        participant = self.get_object(pk)
        if participant is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ThreadParticipantSerializer(participant, data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)  # Automatically set created_by
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        participant = self.get_object(pk)
        if participant is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        participant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ThreadMessagesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, thread_id):
        thread = get_object_or_404(Thread, id=thread_id)

        messages = Message.objects.filter(thread=thread, is_deleted=False).order_by(
            "created_at"
        )

        serializer = ThreadMessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, thread_id):
        thread = get_object_or_404(Thread, id=thread_id)

        serializer = CreateMessageSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(
                CustomUser, id=serializer.validated_data["user"].id
            )
            message = Message.objects.create(
                thread=thread,
                user=user,
                content=serializer.validated_data["content"],
                created_by=user,
            )
            response_serializer = MessageSerializer(message)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ThreadParticipantsAPIView(APIView):
    def get(self, request, thread_id):
        # Fetch the thread
        thread = get_object_or_404(Thread, id=thread_id)

        # Get all participants for the thread
        participants = ThreadParticipant.objects.filter(thread=thread, is_deleted=False)

        # Serialize the participants
        serializer = ParticipantSerializer(participants, many=True)

        # Return the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, thread_id):
        # Fetch the thread
        thread = get_object_or_404(Thread, id=thread_id)

        # Validate and create the participant
        serializer = CreateParticipantSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(
                CustomUser, id=serializer.validated_data["user"].id
            )

            # Check if the participant already exists
            participant, created = ThreadParticipant.objects.get_or_create(
                thread=thread, user=user, defaults={"created_by": request.user}
            )

            response_data = {"thread_id": str(thread.id), "user_id": str(user.id)}
            return Response(
                response_data,
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
