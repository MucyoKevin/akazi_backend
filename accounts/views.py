from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta
import random
from twilio.rest import Client
from django.conf import settings
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
        
        # Send OTP via Twilio
        send_otp_sms(user.phone_number, otp_code)
        
        return Response({
            'message': 'User registered successfully. OTP sent to phone.',
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
            if not user.is_phone_verified:
                return Response({
                    'error': 'Phone number not verified'
                }, status=status.HTTP_400_BAD_REQUEST)
            
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

def send_otp_sms(phone_number, otp_code):
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        
        message = client.messages.create(
            body=f'Your Akazi App verification code is: {otp_code}',
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        
        return message.sid
    except Exception as e:
        # Log the error in production
        print(f"Failed to send SMS: {e}")
        return None
