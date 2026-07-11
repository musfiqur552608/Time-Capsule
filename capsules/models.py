from django.db import models

class Capsule(models.Model):
    class Status(models.TextChoices):
        SEALED = "sealed", "Sealed"
        UNLOCKED = "unlocked", "Unlocked"
        DELIVERED = "delivered", "Delivered"
    
    recipient_email = models.EmailField()
    title = models.CharField(max_length=120)
    message = models.TextField()
    unlock_at = models.DateTimeField()
    status = models.CharField(
        max_length = 10, choices = Status.choices, default = Status.SEALED
    )
    created_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["unlock_at"]

    def __str__(self):
        return f"{self.title} -> {self.unlock_at:%Y-%m-%d %H:%M}"
        


    
