from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from datetime import date
from django.db.models import Q
from .models import ImagePost, Admission, Testimonial
from .serializers import (
    ImagePostSerializer, AdmissionSerializer, TestimonialSerializer,
    RegisterSerializer, LoginSerializer, UserSerializer, UserProfileSerializer,
)

def _format_exception_response(exc):
    # Keep validation errors as 400 so the frontend can show actionable feedback.
    if isinstance(exc, ValidationError):
        return Response({"error": exc.detail}, status=status.HTTP_400_BAD_REQUEST)

    error_msg = str(exc)
    lowered = error_msg.lower()
    if any(token in lowered for token in ["cloudinary", "api_key", "api key", "api_secret", "api secret"]):
        error_msg = "Cloudinary is not configured correctly on the server. Set CLOUDINARY_URL or CLOUDINARY_* env vars."
    return Response({"error": error_msg}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ImagePostListCreate(generics.ListCreateAPIView):
    queryset = ImagePost.objects.all().order_by('-created_at')
    serializer_class = ImagePostSerializer

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            return _format_exception_response(e)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return _format_exception_response(e)

class ImagePostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ImagePost.objects.all()
    serializer_class = ImagePostSerializer

class AdmissionListCreate(generics.ListCreateAPIView):
    queryset = Admission.objects.all().order_by('-date_joined')
    serializer_class = AdmissionSerializer

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            return _format_exception_response(e)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return _format_exception_response(e)

class AdmissionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Admission.objects.all()
    serializer_class = AdmissionSerializer

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

class OverdueAdmissionList(generics.ListAPIView):
    serializer_class = AdmissionSerializer

    def get_queryset(self):
        today = date.today()
        all_members = Admission.objects.all()
        overdue_ids = []
        
        for member in all_members:
            anchor_date = member.date_joined
            if not anchor_date:
                continue
            
            # Use last_payment_date if exists, otherwise use join_date to start counting
            last_valid_payment = member.last_payment_date or anchor_date
            
            # Calculate the "Next Due Date"
            # It should be the same day of the month as joinedDate, but in the next month after last_payment
            next_due_year = last_valid_payment.year
            next_due_month = last_valid_payment.month + 1
            
            if next_due_month > 12:
                next_due_month = 1
                next_due_year += 1
            
            import calendar
            last_day_of_next_month = calendar.monthrange(next_due_year, next_due_month)[1]
            next_due_day = min(anchor_date.day, last_day_of_next_month)
            
            next_due_date = date(next_due_year, next_due_month, next_due_day)
            
            # PRO ALGORITHM: If today is past the NEXT due date, they are definitely overdue!
            if today >= next_due_date:
                overdue_ids.append(member.id)
                
        return Admission.objects.filter(id__in=overdue_ids).order_by('name')

class TestimonialListCreate(generics.ListCreateAPIView):
    queryset = Testimonial.objects.all().order_by('-created_at')
    serializer_class = TestimonialSerializer

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            return _format_exception_response(e)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return _format_exception_response(e)


class TestimonialDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer


# ─── Auth Views ─────────────────────────────────────────────────────────────────

class RegisterView(APIView):
    """POST /api/auth/register/  →  creates user + profile, returns token."""

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {"token": token.key, "user": UserSerializer(user).data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """POST /api/auth/login/  →  returns token for valid credentials."""

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {"token": token.key, "user": UserSerializer(user).data}
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """POST /api/auth/logout/  →  deletes the user's token."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"detail": "Logged out."}, status=status.HTTP_204_NO_CONTENT)


class MeView(APIView):
    """GET/PATCH /api/auth/me/  →  retrieve or update current user profile."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def patch(self, request):
        profile = getattr(request.user, 'profile', None)
        if not profile:
            return Response({"detail": "Profile not found."}, status=404)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(UserSerializer(request.user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
