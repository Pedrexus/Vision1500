from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from registration.forms import SignUpForm
from registration.models import MyUser
from registration.tokens import account_activation_token


def home(request):
    return render(request, 'registration/home.html')


def home_logout(request):
    logout(request)
    return redirect('home')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False

            user.save()
            current_site = get_current_site(request)

            message = render_to_string(
                'registration/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(
                        "utf-8"),
                    'token': account_activation_token.make_token(user),
                })

            subject = 'Activate Your MySite Account'
            user.email_user(subject, message)

            return render(request, 'registration/account_activation_sent.html',
                          {'user': user})
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = MyUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('user_home')
    else:
        return render(request, 'registration/account_activation_invalid.html')


def account_activation_sent(request):
    return render(request, 'registration/account_activation_sent.html')