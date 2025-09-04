from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from django.utils import timezone
from .models import User, OTP
from .serializers import (
    UserRegistrationSerializer, UserSerializer, UserProfileUpdateSerializer,
    LoginSerializer, OTPSerializer, OTPVerificationSerializer,
    ChangePasswordSerializer, ForgotPasswordSerializer, ResetPasswordSerializer
)


class RegisterView(APIView):
    """User registration endpoint"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            
            return Response({
                'message': 'User registered successfully',
                'user': UserSerializer(user).data,
                'tokens': {
                    'access': str(access_token),
                    'refresh': str(refresh)
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """User login endpoint"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            
            return Response({
                'message': 'Login successful',
                'user': UserSerializer(user).data,
                'tokens': {
                    'access': str(access_token),
                    'refresh': str(refresh)
                }
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """User logout endpoint"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """User profile view and update"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class UserProfileUpdateView(generics.UpdateAPIView):
    """Update user profile information"""
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class GenerateOTPView(APIView):
    """Generate OTP for phone/email verification"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = OTPSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            otp = serializer.save()
            
            # TODO: Send OTP via SMS/Email
            # For development, we'll return the OTP in response
            return Response({
                'message': f'OTP sent to your {otp.otp_type}',
                'otp_code': otp.otp_code,  # Remove this in production
                'expires_at': otp.expires_at
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    """Verify OTP for phone/email verification"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            otp = serializer.validated_data['otp']
            otp.is_used = True
            otp.save()
            
            # Mark user as verified
            user = request.user
            if serializer.validated_data['otp_type'] == 'phone':
                user.is_verified = True
                user.save()
            
            return Response({
                'message': f'{serializer.validated_data["otp_type"].title()} verified successfully'
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    """Change user password"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
    """Send OTP for password reset"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            
            # Generate OTP
            otp_code = ''.join(random.choices(string.digits, k=6))
            expires_at = timezone.now() + timedelta(minutes=10)
            
            OTP.objects.create(
                user=user,
                otp_type='email',
                otp_code=otp_code,
                expires_at=expires_at
            )
            
            # TODO: Send OTP via email
            return Response({
                'message': 'OTP sent to your email',
                'otp_code': otp_code  # Remove this in production
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    """Reset password using OTP"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            otp_code = serializer.validated_data['otp_code']
            new_password = serializer.validated_data['new_password']
            
            # Get OTP and user
            otp = OTP.objects.get(otp_code=otp_code, otp_type='email', is_used=False)
            user = otp.user
            
            # Update password
            user.set_password(new_password)
            user.save()
            
            # Mark OTP as used
            otp.is_used = True
            otp.save()
            
            return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_dashboard(request):
    """User dashboard data"""
    user = request.user
    
    # Get user's recent orders
    from orders.models import Order
    recent_orders = Order.objects.filter(user=user).order_by('-created_at')[:5]
    
    # Get user's cart items
    from orders.models import Cart
    cart_items = Cart.objects.filter(user=user)
    
    dashboard_data = {
        'user': UserSerializer(user).data,
        'recent_orders': [
            {
                'order_number': order.order_number,
                'status': order.status,
                'total_amount': order.total_amount,
                'created_at': order.created_at
            }
            for order in recent_orders
        ],
        'cart_items_count': cart_items.count(),
        'total_spent': sum(order.total_amount for order in Order.objects.filter(user=user, status='delivered'))
    }
    
    return Response(dashboard_data, status=status.HTTP_200_OK)