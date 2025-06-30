from django.urls import path, include
from authentication import views

app_name = 'authentication'

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'), # Registration page for new users
    path('signin/', views.SigninView.as_view(), name='signin'), # Login page for existing users
    path('signout/', views.SignOutView.as_view(), name='signout'), # Logout functionality
    path('verify/', views.VerifyView.as_view(), name='verify'), # This is for OTP verification

    path('accounts/', include('django.contrib.auth.urls')), # This includes login, logout, password change, etc.

]