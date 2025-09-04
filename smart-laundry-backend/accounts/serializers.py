from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User, OTP
import random
import string
from datetime import datetime, timedelta
from django.utils import timezone


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('email', 'phone', 'first_name', 'last_name', 'password', 'password_confirm')
        extra_kwargs = {
            'email': {'required': True},
            'phone': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match.")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    full_address = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = ('id', 'email', 'phone', 'first_name', 'last_name', 'full_name', 
                 'role', 'is_verified', 'address_line1', 'address_line2', 'city', 
                 'state', 'pincode', 'country', 'full_address', 'date_joined')
        read_only_fields = ('id', 'email', 'role', 'is_verified', 'date_joined')


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'address_line1', 'address_line2', 
                 'city', 'state', 'pincode', 'country')
    
    def validate_phone(self, value):
        if User.objects.filter(phone=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("Phone number already exists.")
        return value


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid email or password.')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Must include email and password.')


class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ('otp_type', 'otp_code')
        read_only_fields = ('otp_code',)
    
    def create(self, validated_data):
        # Generate 6-digit OTP
        otp_code = ''.join(random.choices(string.digits, k=6))
        user = self.context['request'].user
        
        # Set expiration time (10 minutes from now)
        expires_at = timezone.now() + timedelta(minutes=10)
        
        # Create OTP
        otp = OTP.objects.create(
            user=user,
            otp_type=validated_data['otp_type'],
            otp_code=otp_code,
            expires_at=expires_at
        )
        
        # TODO: Send OTP via SMS/Email
        # For now, we'll just return it (in production, remove this)
        validated_data['otp_code'] = otp_code
        return otp


class OTPVerificationSerializer(serializers.Serializer):
    otp_code = serializers.CharField(max_length=6)
    otp_type = serializers.ChoiceField(choices=[('phone', 'Phone'), ('email', 'Email')])
    
    def validate(self, attrs):
        user = self.context['request'].user
        otp_code = attrs.get('otp_code')
        otp_type = attrs.get('otp_type')
        
        try:
            otp = OTP.objects.get(
                user=user,
                otp_code=otp_code,
                otp_type=otp_type,
                is_used=False
            )
            
            if otp.is_expired():
                raise serializers.ValidationError('OTP has expired.')
            
            attrs['otp'] = otp
            return attrs
            
        except OTP.DoesNotExist:
            raise serializers.ValidationError('Invalid OTP.')


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password])
    new_password_confirm = serializers.CharField()
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("New passwords don't match.")
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is incorrect.')
        return value
    
    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError('User with this email does not exist.')


class ResetPasswordSerializer(serializers.Serializer):
    otp_code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(validators=[validate_password])
    new_password_confirm = serializers.CharField()
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("Passwords don't match.")
        return attrs
    
    def validate_otp_code(self, value):
        try:
            otp = OTP.objects.get(
                otp_code=value,
                otp_type='email',
                is_used=False
            )
            
            if otp.is_expired():
                raise serializers.ValidationError('OTP has expired.')
            
            return value
            
        except OTP.DoesNotExist:
            raise serializers.ValidationError('Invalid OTP.')