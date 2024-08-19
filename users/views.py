from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView
import secrets, string, random
from django.contrib.auth.hashers import make_password
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


# Create your views here.
class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        token = secrets.token_urlsafe(16)
        user.email_token = token
        user.save()

        print(f'Token saved in database: {user.email_token}')  # Проверка сохраненного токена

        host = self.request.get_host()
        url = f'http://{host}/users/email_confirm/{token}'

        send_mail(
            subject='Добро пожаловать на наш сайт! Подтвердите почту',
            message=f'Спасибо за регистрацию на нашем сайте. Перейдите по ссылке {url}',
            from_email=None,
            recipient_list=[form.cleaned_data.get('email')],
            fail_silently=False,
        )

        return super().form_valid(form)


def email_verification_email(request, token):
    user = get_object_or_404(User, email_token=token)
    user.is_active = True
    user.email_token = None
    user.save()
    return redirect(reverse('users:profile'))


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class PasswordResetView(View):
    @staticmethod
    def get(request):
        return render(request, 'users/password_reset.html')

    @staticmethod
    def post(request):
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            user.password = make_password(new_password)
            user.save()
            send_mail(
                "Восстановление пароля",
                f"Ваш новый пароль: {new_password}",
                "SkyStoreClub@yandex.ru",
                [email],
                fail_silently=False,
            )
            return redirect('users:login')
        except User.DoesNotExist:
            return render(request, 'users/password_reset.html', {'error': 'Пользователь с таким адресом не найден.'})