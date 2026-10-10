from rest_framework import status, views, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.utils.crypto import get_random_string
from .models import User, UserProfile
from .forms import CustomUserCreationForm, CustomUserChangeForm, UserProfileForm
from .serializers import UserSerializer, UserProfileSerializer


class RegisterView(views.APIView):
    """User registration endpoint."""
    
    permission_classes = [AllowAny]

    def post(self, request):
        """Register a new user."""
        data = request.data.copy()

        data['department'] = data.get('department') or 'BSIT'
        data['password1'] = data.get('password1') or data.get('password')
        data['password2'] = data.get('password2') or data.get('password_confirm') or data.get('password')

        if not data.get('username') and data.get('email'):
            email_base = data['email'].split('@')[0]
            username = email_base[:150]
            while User.objects.filter(username=username).exists():
                username = f"{email_base}_{get_random_string(5)}"
            data['username'] = username

        form = CustomUserCreationForm(data)
        if form.is_valid():
            user = form.save()
            login(request, user)
            UserProfile.objects.get_or_create(user=user)
            return Response({
                'message': 'User registered successfully',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(views.APIView):
    """User login endpoint."""
    
    permission_classes = [AllowAny]

    def post(self, request):
        """Authenticate user and return user data."""
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')

        user = None
        if username:
            user = authenticate(request, username=username, password=password)
        elif email:
            user_obj = User.objects.filter(email=email).first()
            if user_obj:
                user = authenticate(request, username=user_obj.username, password=password)

        if user is not None:
            login(request, user)
            return Response({
                'message': 'Login successful',
                'user': UserSerializer(user).data,
                'access': 'token',
                'user_id': user.id,
                'email': user.email
            }, status=status.HTTP_200_OK)
        return Response({
            'error': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(views.APIView):
    """User logout endpoint."""
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Logout user."""
        logout(request)
        return Response({
            'message': 'Logout successful'
        }, status=status.HTTP_200_OK)


class CurrentUserView(views.APIView):
    """Get current authenticated user."""
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return current user data."""
        return Response(UserSerializer(request.user).data)


class UserProfileView(generics.RetrieveAPIView):
    """View user profile by ID."""
    
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserProfileUpdateView(views.APIView):
    """Update current user profile."""
    
    permission_classes = [IsAuthenticated]

    def put(self, request):
        """Update user profile."""
        user = request.user
        form = CustomUserChangeForm(request.data, instance=user)
        if form.is_valid():
            user = form.save()
            return Response({
                'message': 'Profile updated successfully',
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentListView(generics.ListAPIView):
    """List all students with profiles."""
    
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    
    def get_queryset(self):
        return User.objects.filter(role=User.Role.STUDENT, is_active=True)


class FacultyListView(generics.ListAPIView):
    """List all faculty members."""
    
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    
    def get_queryset(self):
        return User.objects.filter(role=User.Role.FACULTY, is_active=True)
