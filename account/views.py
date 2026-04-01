from copy import replace
from datetime import datetime, timedelta
from django.utils import timezone
import email
import token
import token
from urllib import request

from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from rest_framework import status

from account.models import Profile
from .serializers import SignupSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
# Create your views here.

@api_view(['Post'])
def register(request):
    data = request.data 
    usre = SignupSerializer(data=data)
    
    
    if usre.is_valid():
        if not User.objects.filter(username=data['email']).exists():
            usre = User.objects.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                username=data['email'],
                password=make_password(data['password'])
            )
            usre.save()
            return Response(
                {'details':'Your account is registered'},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'error':'This email already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
    else:
        return Response(usre.errors)
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])

def currentUser(request):
    user = UserSerializer(request.user , many=False)
    return Response(user.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])

def updata_User(request):
    user = request.user
    data = request.data 
    
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.email = data.get('email', user.email)
    user.username = data.get('email', user.username)
    if data.get('password') and data['password'] != '':
        user.password = make_password(data['password'])
        
        
    user.save()
    serializer = UserSerializer(user , many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

def get_current_host(request):
    protocol = request.is_secure() and 'https' or 'http'
    host = request.get_host()
    return f"{protocol}://{host}"

@api_view(['POST'])
def forgot_password(request):
    data = request.data
    email = data.get('email')
    user = User.objects.filter(email=email).first()

    if not user:
        return Response(
            {'error': 'No user found with this email address'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    profile, created = Profile.objects.get_or_create(user=user)

    token = get_random_string(40).replace('\n', '').replace('\r', '')
    expire_date = timezone.now() + timedelta(minutes=30) 
    profile.reset_password_token = token
    profile.reset_password_token_expire = expire_date
    profile.save()

    host = get_current_host(request)
    link = f"http://127.0.0.1:8000/api/reset_password/{token}/"
    link = link.strip()
    body = f'Your password reset link is: {link}'
    
    try:
        send_mail(
            "Password Reset From Ecommerce",
            body,
            "noreply@ecommerce.com",
            [email],
            fail_silently=False,
        )
    except Exception as e:
        return Response({'error': 'Failed to send email, please try again later'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'details': f'Password reset sent to {email}'}, status=status.HTTP_200_OK)




@api_view(['POST'])
def reset_password(request, token):
    data = request.data
    email = data.get('email')
    user = get_object_or_404(User, profile__reset_password_token=token)

    if user.profile.reset_password_token_expire.replace(tzinfo=None) < datetime.now(): 
        return Response(
            {'error': 'Token is expired'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    if data['password'] != data['confirm_password']:
        return Response(
            {'error': 'Password and confirm password do not match'}, 
            status=status.HTTP_400_BAD_REQUEST
        )  

    user.password = make_password(data['password'])
    
    user.profile.reset_password_token = ""
    user.profile.reset_password_token_expire = None
    user.profile.save()
    user.save()
    return Response({'details': f'Password reset done'}, status=status.HTTP_200_OK)