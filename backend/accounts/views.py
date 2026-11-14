from django.contrib.auth.models import User
from django.db import transaction
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate, get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.exceptions import TokenError
from .models import UserProfile

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):

    email = request.data.get('email')
    password = request.data.get('password')
    # Check whether both fields are provided
    if not email or not password:
        return Response(
            {'error':'Email and password are required.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    # Find user using email
    try:
        user = User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        return Response(
            {'error': 'Invalid email or password.'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    # Verify password
    authenticated_user = authenticate(
        request,
        username=user.get_username(),
        password=password
    )
    if authenticated_user is None:
        return Response(
            {'error': 'Invalid email or password.'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    # Generate JWT tokens
    refresh = RefreshToken.for_user(authenticated_user)
    return Response({
        'message': 'Login successful!',
        'user': {
            'id': authenticated_user.id,
            'username': authenticated_user.get_username(),
            'email': authenticated_user.email
        },
        'tokens': {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    user = request.user
    return Response({
        'message': 'Authenticated successfully!',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    refresh_token = request.data.get('refresh')
    if not refresh_token:
        return Response(
            {'error': 'Refresh token is required.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(
            {'message': 'Logout successful!'},
            status=status.HTTP_200_OK
        )
    except TokenError:
        return Response(
            {'error': 'Invalid or expired refresh token.'},
            status=status.HTTP_400_BAD_REQUEST
        )
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    full_name = request.data.get('full_name', '').strip()
    email = request.data.get('email', '').strip().lower()
    phone = request.data.get('phone', '').strip()
    password = request.data.get('password')
    confirm_password = request.data.get('confirm_password')
    # Check required fields
    if not all([full_name, email, phone, password, confirm_password]):
        return Response(
            {'error': 'All fields are required.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    # Check name
    if len(full_name.split()) < 2:
        return Response(
            {'error': 'Please enter your full name.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    # Check email uniqueness
    if User.objects.filter(email__iexact=email).exists():
        return Response(
            {'error': 'An account with this email already exists.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    # Check phone number
    if not phone.isdigit() or len(phone) != 10:
        return Response(
            {'error': 'Enter a valid 10-digit phone number.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    # Check password confirmation
    if password != confirm_password:
        return Response(
            {'error': 'Passwords do not match.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    # Validate password strength
    try:
        validate_password(password)
    except ValidationError as error:
        return Response(
            {'error': error.messages},
            status=status.HTTP_400_BAD_REQUEST
        )
    # Create user and profile together
    try:
        with transaction.atomic():
            first_name, last_name = full_name.split(' ', 1)
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            UserProfile.objects.create(
                user=user,
                phone=phone
            )
        return Response(
            {'message': 'Registration successful! You can now log in.'},
            status=status.HTTP_201_CREATED
        )
    except Exception:
        return Response(
            {'error': 'Unable to create account. Please try again.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )