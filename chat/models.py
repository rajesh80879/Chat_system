import uuid
from django.db import models
from users.models import CustomUser


class BaseModel(models.Model):
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_created_by",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Thread(BaseModel):  # Inherit from BaseModel
    ENTITY_TYPES = [
        ("ORDER", "Order"),
        ("ORDERLINE", "Order Line"),
        ("SUPPLIER", "Supplier"),
        ("PAYMENT", "Payment"),
        ("STOCK", "Stock"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    entity_type = models.CharField(max_length=50, choices=ENTITY_TYPES)
    entity_id = models.CharField(max_length=50)
    title = models.TextField()

    class Meta:
        indexes = [models.Index(fields=["entity_type", "entity_id"])]

    def __str__(self):
        return f"{self.title}"


class Message(BaseModel):  # Inherit from BaseModel
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    thread = models.ForeignKey(
        Thread, related_name="messages", on_delete=models.CASCADE
    )
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"Message by {self.user} in Thread {self.thread.title}"


class ThreadParticipant(BaseModel):  # Inherit from BaseModel
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    thread = models.ForeignKey(
        Thread, related_name="participants", on_delete=models.CASCADE
    )
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)

    def __str__(self):
        return f"Participant {self.user} in Thread {self.thread.title}"
