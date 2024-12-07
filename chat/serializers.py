from rest_framework import serializers
from .models import Thread, Message, ThreadParticipant


class ThreadSerializer(serializers.ModelSerializer):
    thread_id = serializers.UUIDField(source="id")

    class Meta:
        model = Thread
        fields = [
            "thread_id",
            "entity_type",
            "entity_id",
            "title",
            "created_by",
            "created_at",
        ]


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "thread", "user", "content", "created_by", "created_at"]


class ThreadParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThreadParticipant
        fields = ["id", "thread", "user", "created_by", "created_at"]


class ThreadMessageSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(source="user.id")
    user_name = serializers.CharField(source="user.name")
    message_id = serializers.UUIDField(source="id")

    class Meta:
        model = Message
        fields = ["message_id", "user_id", "user_name", "content", "created_at"]


class CreateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["user", "content"]


class CreateParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThreadParticipant
        fields = ["user"]


class ParticipantSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(source="user.id")
    user_name = serializers.CharField(source="user.name")

    class Meta:
        model = ThreadParticipant
        fields = ["user_id", "user_name"]
