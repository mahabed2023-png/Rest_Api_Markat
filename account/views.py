from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status
from .serializers import SignupSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
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

