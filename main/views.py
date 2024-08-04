from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.core import paginator
from django.utils import timezone
from accounts.serializers import UserSerializer
from .models import FriendRequest, Friends
from .serializers import FriendRequestSerializer, FriendsSerializer

def paginate(data, records, page):
    data_list = paginator.Paginator(data, records)
    try:
        page_data = data_list.get_page(page)
    except paginator.PageNotAnInteger:
        return Response({'message': "Page number should be an integer"}, status=status.HTTP_400_BAD_REQUEST)
    except paginator.EmptyPage:
        return Response({'message': f'Empty page. Total pages are {data_list.num_pages}'}, status=status.HTTP_400_BAD_REQUEST)
    
    return page_data


class ProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except:
            return Response({"message": "No such user exists"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, user_id):
        data = request.data

        try:
            user = User.objects.get(id=user_id)

        except User.DoesNotExist:
            return Response({"message": "No such user exists"}, status=status.HTTP_404_NOT_FOUND)
             
        if request.user != user:
            return Response({'message': 'You do not have permission to edit this profile'}, status=status.HTTP_403_FORBIDDEN)
        
        username = data.get('username')
        if not username:
            return Response({"message": "Username cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)
        
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return Response({"message": "Profile updated successfully"}, status=status.HTTP_200_OK)

class UsersView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        value = request.GET.get('search')
        if value:
            users = User.objects.filter(
                                        Q(email__icontains=value) | 
                                        Q(first_name__icontains=value) |
                                        Q(last_name__icontains=value) |
                                        Q(username__icontains=value)
                                    ).order_by('id')
            page =  request.GET.get('page', 1)
            page_data = paginate(users, 10, page)
            if not isinstance(page_data, Response):            
                serializer = UserSerializer(page_data.object_list, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return page_data
        return Response({'message': 'No search data'}, status=status.HTTP_400_BAD_REQUEST)
    
class FriendRequestView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        frnd_req = FriendRequest.objects.filter(receiver=request.user).order_by('-created_at')
        page = request.GET.get('page', 1)
        page_data = paginate(frnd_req, 10, page)
        if not isinstance(page_data, Response):
            serializer = FriendRequestSerializer(page_data.object_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return page_data
    
    def post(self, request):
        data = request.data
        recipient = data.get('recipient')
        try:
            receiver = User.objects.get(id=recipient)
        except User.DoesNotExist:
            return Response({'message': 'Invalid user'}, status=status.HTTP_400_BAD_REQUEST)
        
        if receiver == request.user:
            return Response({'message': "You can't send friend request to yourself"}, status=status.HTTP_400_BAD_REQUEST)
        
        if Friends.objects.filter(user=request.user, friend=receiver).exists():
            return Response({'message': f'{receiver.username} is already your friend'}, status=status.HTTP_400_BAD_REQUEST)
        
        req_obj = FriendRequest.objects.filter(sender=request.user, receiver=receiver)
        if req_obj.exists():
            return Response({'message': f'A friend request has already been sent to {receiver.username} and is currently {req_obj.first().get_status_display()}.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user_req = FriendRequest.objects.filter(sender=request.user).order_by('-created_at')[:3]

        if len(user_req) == 3 and (timezone.now() - user_req.last().created_at).seconds < 60:
            return Response({'message': 'You cannot send more than 3 requests within a minute'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        FriendRequest.objects.create(
            sender = request.user,
            receiver = receiver,
        )

        return Response({'message': 'Request sent successfully'}, status=status.HTTP_200_OK)
    
class SentFriendRequestView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        frnd_req = FriendRequest.objects.filter(sender = request.user).order_by('-created_at')
        page = request.GET.get('page', 1)
        page_data = paginate(frnd_req, 10, page)
        if not isinstance(page_data, Response):
            serializer = FriendRequestSerializer(page_data.object_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return page_data

class RespondFriendRequest(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        sender_id = data.get('sender')
        try:
            sender = User.objects.get(id=sender_id)
        except:
            return Response({'message': 'Invalid user'}, status=status.HTTP_400_BAD_REQUEST)
        
        req_id = data.get('req_id')
        try:
            req_obj = FriendRequest.objects.get(id=req_id)
        except:
            return Response({'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
        
        req_status = data.get('status')
        if not isinstance(req_status, bool):
            return Response({'message': 'Invalid reponse to a friend request'}, status=status.HTTP_400_BAD_REQUEST)
        
        if req_status:
            req_obj.status = FriendRequest.RequestStatus.ACCEPTED
            if not Friends.objects.filter(user=request.user, friend=sender).exists():
                Friends.objects.create(
                    user=request.user,
                    friend=sender
                )
                Friends.objects.create(
                    user=sender,
                    friend=request.user
                )
            
            req_obj.save()
            return Response({'message': 'Friend request accepted'}, status=status.HTTP_200_OK)
        else:
            req_obj.status = FriendRequest.RequestStatus.REJECTED
            req_obj.save()
            return Response({'message': 'Friend request rejected'}, status=status.HTTP_200_OK)

class FriendsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        friends = Friends.objects.select_related('friend').filter(user=user).order_by('-created_on')
        page = request.GET.get('page', 1)
        page_data = paginate(friends, 10, page)
        if not isinstance(page_data, Response):
            serializer = FriendsSerializer(page_data.object_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return page_data