from django.db import models
from django.contrib.auth.models import User

class FriendRequest(models.Model):
    class RequestStatus(models.IntegerChoices):
        PENDING = 1, "Pending"
        ACCEPTED = 2, "Accepted"
        REJECTED = 3, "Rejected"
    
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    status = models.IntegerField(choices=RequestStatus.choices, default=RequestStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'FriendRequests'

class Friends(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend')
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Friends'