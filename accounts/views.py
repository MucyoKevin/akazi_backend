from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta
import random
from django.conf import settings
from django.core.mail import send_mail
from .models import User, OTPVerification
from .serializers import UserRegistrationSerializer, OTPVerificationSerializer, UserProfileSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Generate and send OTP
        otp_code = str(random.randint(100000, 999999))
        expires_at = timezone.now() + timedelta(minutes=10)
        
        OTPVerification.objects.create(
            user=user,
            otp_code=otp_code,
            expires_at=expires_at
        )
        
        # Send OTP via Brevo SMTP email (fallback to phone if email missing)
        send_otp_email(user, otp_code)
        
        # TEMPORARILY: Mark phone as verified for testing
        user.is_phone_verified = True
        user.save()
        
        return Response({
            'message': 'User registered successfully. Phone verification temporarily disabled for testing.',
            'user_id': user.id
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp(request):
    user_id = request.data.get('user_id')
    otp_code = request.data.get('otp_code')
    
    try:
        user = User.objects.get(id=user_id)
        otp_verification = OTPVerification.objects.filter(
            user=user,
            otp_code=otp_code,
            is_verified=False,
            expires_at__gt=timezone.now()
        ).first()
        
        if otp_verification:
            otp_verification.is_verified = True
            otp_verification.save()
            
            user.is_phone_verified = True
            user.save()
            
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'message': 'Phone verified successfully',
                'token': token.key,
                'user': UserProfileSerializer(user).data
            })
        else:
            return Response({
                'error': 'Invalid or expired OTP'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    except User.DoesNotExist:
        return Response({
            'error': 'User not found'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    phone_number = request.data.get('phone_number')
    password = request.data.get('password')
    
    try:
        user = User.objects.get(phone_number=phone_number)
        if user.check_password(password):
            # TEMPORARILY: Skip phone verification check for testing
            # if not user.is_phone_verified:
            #     return Response({
            #         'error': 'Phone number not verified'
            #     }, status=status.HTTP_400_BAD_REQUEST)
            
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserProfileSerializer(user).data
            })
        else:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    except User.DoesNotExist:
        return Response({
            'error': 'User not found'
        }, status=status.HTTP_404_NOT_FOUND)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    
    def get_object(self):
        return self.request.user

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    """
    Delete the authenticated user and all associated data.
    This will cascade delete all related records due to CASCADE constraints.
    """
    try:
        user = request.user
        user_id = user.id
        username = user.username
        
        # Delete the user (this will cascade delete all related records)
        user.delete()
        
        return Response({
            'message': f'User {username} (ID: {user_id}) and all associated data have been successfully deleted.',
            'deleted_user_id': user_id,
            'deleted_username': username
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': f'Failed to delete user: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user_by_id(request, user_id):
    """
    Delete a specific user by ID (admin functionality).
    Only allows users to delete themselves or admin users.
    """
    try:
        current_user = request.user
        target_user = User.objects.get(id=user_id)
        
        # Users can only delete themselves, unless they are staff/admin
        if current_user.id != user_id and not current_user.is_staff:
            return Response({
                'error': 'You can only delete your own account'
            }, status=status.HTTP_403_FORBIDDEN)
        
        username = target_user.username
        target_user.delete()
        
        return Response({
            'message': f'User {username} (ID: {user_id}) and all associated data have been successfully deleted.',
            'deleted_user_id': user_id,
            'deleted_username': username
        }, status=status.HTTP_200_OK)
        
    except User.DoesNotExist:
        return Response({
            'error': 'User not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': f'Failed to delete user: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def send_otp_email(user, otp_code):
    subject = 'Akazi Verification Code'
    message = f'Your Akazi verification code is: {otp_code}. It expires in 10 minutes.'
    recipient = user.email
    if not recipient:
        # If no email on the account, do nothing (or extend to SMS provider later)
        return None
    try:
        return send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient], fail_silently=False)
    except Exception as e:
        print(f"Failed to send OTP email: {e}")
        return None
