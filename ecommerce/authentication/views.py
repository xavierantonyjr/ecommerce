from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views import View
from .forms import SignUpForm, SignInForm
from .models import CustomUser



# Create your views here.
class SignupView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        print(request.POST)
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            user.generate_otp()

            send_mail(
                'Django OTP Verification',
                f'Your OTP is: {user.otp}',
                'noreply@example.com',
                [user.email],
                fail_silently=False,
            )

            messages.success(request, "OTP sent to your email.")
            return redirect('authentication:verify')

        return render(request, 'signup.html', {'form': form})


class SigninView(View):
    def get(self, request):
        form = SignInForm()
        return render(request, 'signin.html', {'form': form})

    def post(self, request):
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is None:
                form.add_error(None, 'Invalid username or password.')
            elif not user.is_active:
                form.add_error(None, 'Account is not active. Please verify your email.')
            else:
                login(request, user)
                return redirect('shop:categories')

        return render(request, 'signin.html', {'form': form})

class SignOutView(View):
    def get(self, request):
        logout(request)
        return redirect('shop:categories')

class VerifyView(View):
    def get(self, request):
        return render(request, 'verify.html')

    def post(self, request):
        otp = request.POST.get('otp')
        try:
            user = CustomUser.objects.get(otp=otp)
            user.is_active = True
            user.is_verified = True
            user.otp = None
            user.save()
            messages.success(request, 'Email verified. You can now log in.')
            return redirect('authentication:signin')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Invalid OTP')
            return redirect('authentication:verify')
