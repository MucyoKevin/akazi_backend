from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('login/', views.login, name='login'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('me/', views.UserProfileView.as_view(), name='me'),  # Alias for profile
    path('delete/', views.delete_user, name='delete_user'),
    path('delete/<int:user_id>/', views.delete_user_by_id, name='delete_user_by_id'),
]
