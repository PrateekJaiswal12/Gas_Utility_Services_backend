# accounts/views.py

from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import CustomUser
from utility_services.models import ServiceRequest
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.contrib.auth import login, authenticate
from django import forms
import uuid

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    name = forms.CharField(max_length=100, required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'name', 'phone_number', 'address', 'password1', 'password2')

# Admin API endpoints
@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_list_users(request):
    users = CustomUser.objects.all()
    data = [{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'name': user.name,
        'phone_number': user.phone_number,
        'address': user.address,
        'customer_id': user.customer_id,
        'is_active': user.is_active,
        'is_staff': user.is_staff,
        'is_superuser': user.is_superuser,
        'date_joined': user.date_joined
    } for user in users]
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_create_user(request):
    form = CustomUserCreationForm(request.data)
    if form.is_valid():
        user = form.save(commit=False)
        user.customer_id = f"CUST{uuid.uuid4().hex[:8].upper()}"
        user.save()
        return Response({
            'message': 'User created successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'name': user.name,
                'customer_id': user.customer_id
            }
        }, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def admin_user_detail(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'name': user.name,
            'phone_number': user.phone_number,
            'address': user.address,
            'customer_id': user.customer_id,
            'is_active': user.is_active,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'date_joined': user.date_joined
        }
        return Response(data)

    elif request.method == 'PUT':
        data = request.data
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.name = data.get('name', user.name)
        user.phone_number = data.get('phone_number', user.phone_number)
        user.address = data.get('address', user.address)
        user.is_active = data.get('is_active', user.is_active)
        user.is_staff = data.get('is_staff', user.is_staff)
        user.is_superuser = data.get('is_superuser', user.is_superuser)
        
        if 'password' in data:
            user.set_password(data['password'])
        
        user.save()
        return Response({'message': 'User updated successfully'})

    elif request.method == 'DELETE':
        # Check if user has any service requests
        if ServiceRequest.objects.filter(customer=user).exists():
            return Response({
                'error': 'Cannot delete user with existing service requests'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Delete user without admin logging
        user.delete()
        return Response({'message': 'User deleted successfully'})

# Regular user endpoints
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def account_info(request):
    user = request.user
    data = {
        'username': user.username,
        'email': user.email,
        'name': user.name,
        'phone_number': user.phone_number,
        'address': user.address,
        'customer_id': user.customer_id
    }
    return Response(data)

@ensure_csrf_cookie
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.data)
        if form.is_valid():
            user = form.save(commit=False)
            user.customer_id = f"CUST{uuid.uuid4().hex[:8].upper()}"
            user.save()
            login(request, user)
            return Response({
                'message': 'Registration successful',
                'user': {
                    'username': user.username,
                    'email': user.email,
                    'name': user.name,
                    'customer_id': user.customer_id
                }
            }, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@ensure_csrf_cookie
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({
                'error': 'Please provide both username and password'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return Response({
                'message': 'Login successful',
                'user': {
                    'username': user.username,
                    'email': user.email,
                    'name': user.name,
                    'customer_id': user.customer_id
                }
            })
        else:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response({'message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
