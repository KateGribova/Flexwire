from datetime import datetime
from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import View
import jwt

from users.forms import CustomUserCreationForm
from users.forms import UserAccountForm
from users.models import CustomUser


def decode_token(token):
    try:
        data = jwt.decode(
            token, settings.SECRET_KEY, algorithms=['HS256'], verify=True
        )
    except jwt.exceptions.ExpiredSignatureError:
        return False, 'Activation time expired'
    except jwt.exceptions.DecodeError:
        return False, 'Incorrect link'
    return True, data


class ActivateUserView(View):
    template_name = 'users/activate.html'

    def get(self, request, token):
        is_decoding_token_correct, result_token_decoding = decode_token(token)
        if not is_decoding_token_correct:
            messages.error(request, result_token_decoding)
            return render(request, self.template_name)

        user = get_object_or_404(
            CustomUser, username=result_token_decoding['username']
        )
        if user.is_active is False:
            user.is_active = True
            user.save()
            messages.success(request, 'Account activated!')
        else:
            messages.success(request, 'Account has already activated before')
        return render(request, self.template_name)


def generate_token(username, expired):
    expired = datetime.now(tz=timezone.utc) + timedelta(hours=expired)
    return jwt.encode(
        {'exp': expired, 'username': username},
        settings.SECRET_KEY,
        algorithm='HS256',
    )


class Register(FormView):
    template_name = 'users/signup.html'
    model = CustomUser
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save(commit=False)

        user.is_active = settings.DEFAULT_USER_ACTIVITY
        user.save()

        if not settings.DEFAULT_USER_ACTIVITY:
            send_mail(
                'Verification account',
                '',
                settings.DEFAULT_FROM_EMAIL,
                [form.cleaned_data['email']],
                html_message=loader.render_to_string(
                    'users/activating_email.html',
                    {
                        'token': generate_token(
                            form.cleaned_data['username'], 24
                        )
                    },
                ),
                fail_silently=False,
            )

        login(self.request, user)
        return super().form_valid(form)


class Profile(DetailView):
    template_name = 'users/profile.html'
    model = CustomUser
    context_object_name = 'user'

    def get(self, request, pk):
        if pk == request.user.id:
            context = {'user': request.user}
            return render(request, self.template_name, context)
        return super().get(request, pk)


class Account(View):
    template_name = 'users/account.html'

    def get(self, request):
        user = request.user
        form = UserAccountForm(instance=user)
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        user = request.user

        form = UserAccountForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
            return redirect('users:profile', request.user.id)

        return render(request, self.template_name, context={'form': form})
