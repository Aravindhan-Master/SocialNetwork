from django.urls import path
from . import views

urlpatterns = [
    path('users', views.UsersView.as_view(), name='users'),
    path('users/<int:user_id>/profile', views.ProfileView.as_view(), name='profile'),
    path('users/<int:user_id>/friends', views.FriendsView.as_view(), name='friends'),
    path('friend-requests', views.FriendRequestView.as_view(), name='friend-req'),
    path('friend-requests/sent', views.SentFriendRequestView.as_view(), name='sent-requests'),
    path('friend-requests/respond', views.RespondFriendRequest.as_view(), name='respond-req'),
]