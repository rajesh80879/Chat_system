from django.urls import path
from .views import (
    ThreadListCreateAPIView,
    ThreadMessagesAPIView,
    ThreadParticipantsAPIView,
    ThreadRetrieveUpdateDestroyAPIView,
    MessageListCreateAPIView,
    MessageRetrieveUpdateDestroyAPIView,
    ThreadParticipantListCreateAPIView,
    ThreadParticipantRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    # Thread endpoints
    path("threads/", ThreadListCreateAPIView.as_view(), name="thread-list"),
    path(
        "threads/<str:pk>/",
        ThreadRetrieveUpdateDestroyAPIView.as_view(),
        name="thread-detail",
    ),
    # Message endpoints
    path("messages/", MessageListCreateAPIView.as_view(), name="message-list"),
    path(
        "messages/<str:pk>/",
        MessageRetrieveUpdateDestroyAPIView.as_view(),
        name="message-detail",
    ),
    path(
        "threads/<uuid:thread_id>/messages",
        ThreadMessagesAPIView.as_view(),
        name="thread-messages",
    ),
    # ThreadParticipant endpoints
    path(
        "participants/",
        ThreadParticipantListCreateAPIView.as_view(),
        name="participant-list",
    ),
    path(
        "participants/<str:pk>/",
        ThreadParticipantRetrieveUpdateDestroyAPIView.as_view(),
        name="participant-detail",
    ),
    path(
        "threads/<uuid:thread_id>/participants",
        ThreadParticipantsAPIView.as_view(),
        name="thread-participants",
    ),
]
