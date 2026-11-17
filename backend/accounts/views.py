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
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.exceptions import TokenError
from .models import UserProfile
from .permissions import IsPatient,IsDoctor,IsClinic,IsAdministrator
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.conf import settings

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

@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    user = request.user
    profile = user.profile
    if request.method == 'PATCH':
        phone = request.data.get('phone')
        if phone:
            if not phone.isdigit() or len(phone) != 10:
                return Response(
                    {'error': 'Enter a valid 10-digit phone number'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            profile.phone = phone
            profile.save()
        return Response({
            'message': 'Profile updated successfully!',
            'phone': profile.phone
        })
    return Response({
        'message': 'Profile fetched successfully!',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'phone': profile.phone,
            'role': profile.role
        }
    })

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
    
@api_view(['GET'])
@permission_classes([IsDoctor])
def doctor_dashboard(request):

    return Response({
        'message': 'Welcome to Doctor Dashboard!',
        'user': request.user.email,
        'role': request.user.profile.role
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsClinic])
def clinic_dashboard(request):
    return Response({
        'message': 'Welcome to Clinic Dashboard!',
        'user': request.user.email,
        'role': request.user.profile.role
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsPatient])
def patient_dashboard(request):

    return Response({
        'message': 'Welcome to Patient Dashboard!',
        'user': request.user.email,
        'role': request.user.profile.role
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAdministrator])
def administrator_dashboard(request):
    return Response({
        'message': 'Welcome to Administrator Dashboard!',
        'user': request.user.email,
        'role': request.user.profile.role
    }, status=status.HTTP_200_OK)

@api_view(['PATCH'])
@permission_classes([IsAdministrator])
def update_user_role(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    new_role = request.data.get('role')
    valid_roles = ['patient', 'doctor', 'clinic', 'administrator']
    if new_role not in valid_roles:
        return Response(
            {'error': 'Invalid role'},
            status=status.HTTP_400_BAD_REQUEST
        )
    profile = user.profile
    profile.role = new_role
    profile.save()
    return Response({
        'message': 'User role updated successfully',
        'user': user.email,
        'new_role': profile.role
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user

    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    confirm_password = request.data.get('confirm_password')

    if not user.check_password(old_password):
        return Response(
            {'error': 'Incorrect current password'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if new_password != confirm_password:
        return Response(
            {'error': 'New passwords do not match'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if len(new_password) < 8:
        return Response(
            {'error': 'Password must contain at least 8 characters'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user.set_password(new_password)
    user.save()

    return Response({
        'message': 'Password changed successfully!'
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    email = request.data.get('email')
    try:
        user = User.objects.get(email=email)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = (
            f"{settings.FRONTEND_URL}/frontend/reset-password/reset.html"
            f"?uid={uid}&token={token}"
        )
        send_mail(
            'MedAssist AI - Password Reset',
            f'Click this link to reset your password: {reset_link}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
        )
    except User.DoesNotExist:
        pass
    return Response({
        'message': 'If the account exists, a password reset email has been sent.'
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    uid = request.data.get('uid')
    token = request.data.get('token')
    new_password = request.data.get('new_password')
    try:
        user_id = urlsafe_base64_decode(uid).decode()
        user = User.objects.get(pk=user_id)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return Response({'error': 'Invalid reset link'},
                        status=status.HTTP_400_BAD_REQUEST)
    if not default_token_generator.check_token(user, token):
        return Response({'error': 'Invalid or expired reset token'},
                        status=status.HTTP_400_BAD_REQUEST)
    if not new_password or len(new_password) < 8:
        return Response({'error': 'Password must contain at least 8 characters'},
                        status=status.HTTP_400_BAD_REQUEST)
    user.set_password(new_password)
    user.save()
    return Response({'message': 'Password reset successfully!'})
