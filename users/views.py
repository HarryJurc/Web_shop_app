from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from .forms import EmailAuthenticationForm

from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            send_mail(
                'Добро пожаловать на наш сайт!',
                'Спасибо за регистрацию.',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=True,
            )

            messages.success(request, 'Регистрация прошла успешно! Проверьте почту.')
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

class UserLoginView(LoginView):
    authentication_form = EmailAuthenticationForm
    template_name = 'login.html'

class UserLogoutView(LogoutView):
    template_name = 'logout.html'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return response
