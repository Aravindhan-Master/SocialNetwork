from rest_framework.serializers import ModelSerializer
from .models import FriendRequest, Friends

class FriendRequestSerializer(ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = "__all__"

class FriendsSerializer(ModelSerializer):
    class Meta:
        model = Friends
        fields = "__all__"        