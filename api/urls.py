from django.urls import path
from .views import (
    ImagePostListCreate,
    ImagePostDetail,
    AdmissionListCreate,
    AdmissionDetail,
    TestimonialListCreate,
    TestimonialDetail,
)

urlpatterns = [
    path('gallery/', ImagePostListCreate.as_view(), name='gallery-api'),
    path('gallery/<int:pk>/', ImagePostDetail.as_view(), name='gallery-detail'),
    path('admissions/', AdmissionListCreate.as_view(), name='admissions-api'),
    path('admissions/<int:pk>/', AdmissionDetail.as_view(), name='admission-detail'),
    path('testimonials/', TestimonialListCreate.as_view(), name='testimonials-api'),
    path('testimonials/<int:pk>/', TestimonialDetail.as_view(), name='testimonials-detail'),
]
