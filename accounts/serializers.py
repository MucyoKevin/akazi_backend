from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CustomerProfile, ServiceProvider, OTPVerification

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password', 'user_type', 'location']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        
        # Create profile based on user type
        if user.user_type == 'customer':
            CustomerProfile.objects.create(user=user)
        elif user.user_type == 'provider':
            ServiceProvider.objects.create(user=user, bio='', hourly_rate=0)
        
        return user

class OTPVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPVerification
        fields = ['otp_code']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'phone_number', 'location', 'profile_picture', 'is_phone_verified']
        read_only_fields = ['id', 'is_phone_verified']

class ServiceProviderSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    profile_picture = serializers.ImageField(source='user.profile_picture', read_only=True)
    location = serializers.CharField(source='user.location', read_only=True)
    availability_display = serializers.CharField(source='get_availability_status_display', read_only=True)
    
    class Meta:
        model = ServiceProvider
        fields = ['id', 'user', 'username', 'profile_picture', 'location', 'bio', 
                 'hourly_rate', 'is_available', 'availability_status', 'availability_display',
                 'rating', 'total_reviews', 'is_verified', 'years_experience', 
                 'completed_jobs', 'response_rate']

class ServiceProviderDetailSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    profile_picture = serializers.ImageField(source='user.profile_picture', read_only=True)
    location = serializers.CharField(source='user.location', read_only=True)
    availability_display = serializers.CharField(source='get_availability_status_display', read_only=True)
    services_offered = serializers.StringRelatedField(many=True, read_only=True)
    
    class Meta:
        model = ServiceProvider
        fields = ['id', 'user', 'username', 'profile_picture', 'location', 'bio', 
                 'hourly_rate', 'is_available', 'availability_status', 'availability_display',
                 'rating', 'total_reviews', 'is_verified', 'years_experience', 
                 'completed_jobs', 'response_rate', 'services_offered']

class CustomerProfileSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = CustomerProfile
        fields = ['id', 'user', 'total_bookings', 'rating']
