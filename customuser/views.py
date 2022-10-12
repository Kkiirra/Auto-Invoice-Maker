from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site

from company.models import Currency
from .forms import SignUpForm, LogInForm, CustomUserForm
from django.contrib.auth import get_user_model
from .token import account_activation_token
from .models import User_Account, Countries, CustomUser, DateFormat


def signup(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = False
            user.save()

            User_Account.objects.create(name=user.email, owner=user)
            current_site = get_current_site(request)

            subject = 'Activation link has been sent to your email'
            email_template_name = "registration/registration_email_confirm.txt"
            message = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.id)),
                'token': account_activation_token.make_token(user),
            }
            email = render_to_string(email_template_name, message)
            send_mail(subject, email, 'hello@finum.online', [user, ], fail_silently=False)
            return redirect('customuser:email_send_success')
    else:
        form = SignUpForm()

    context = {'form': form}

    return render(request, 'customuser/signup.html', context)


def signin(request):

    if request.method == 'POST':
        form = LogInForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect('dashboard:dashboard')
            else:
                form.add_error('email', 'Invalid input email or password data')

    else:
        form = LogInForm()

    context = {'form': form}

    return render(request, 'customuser/signin.html', context)


@login_required(login_url='/signin/')
def signout(request):
    logout(request)
    return redirect('customuser:signin')


@login_required(login_url='/signin/')
def settings(request):

    user_account = User_Account.objects.get(owner=request.user)
    countries = Countries.objects.all()
    dates = DateFormat.objects.all()
    currencies = Currency.objects.all()

    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('customuser:settings')

    else:
        form = CustomUserForm(instance=request.user)


    context = {'countries': countries, 'dates': dates, 'currencies': currencies,
               'user_account': user_account, 'form': form}

    return render(request, 'customuser/settings.html', context)


def activate_link(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('integrations:integrations')
    else:
        return redirect('customuser:email_invalid')


@login_required(login_url='/signin/')
def password_reset_request(request):
    user = request.user
    subject = "Password Reset Requested"
    email_template_name = "registration/password_reset_email.txt"
    current_site = get_current_site(request)

    c = {
        "email": user,
        'domain': current_site.domain,
        'site_name': 'Finum',
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "user": user,
        'token': default_token_generator.make_token(user),
        'protocol': 'http',
    }
    email = render_to_string(email_template_name, c)
    try:
        send_mail(subject, email, 'hello@finum.online', [user, ], fail_silently=False)
        return JsonResponse({'mail': 'Successfully sent'}, status=200)
    except Exception:
        return JsonResponse({'mail': 'Something was wrong'}, status=404)


def password_email_request(request):
    if request.method == 'POST':
        password_form = PasswordResetForm(request.POST)
        if password_form.is_valid():
            current_site = get_current_site(request)

            data = password_form.cleaned_data['email']
            user_email = get_user_model().objects.filter(Q(email=data))

            if user_email.exists():
                for user in user_email:
                    subject = 'Password Request'
                    email_template_name = 'registration/password_reset_email.txt'
                    parameters = {
                        'email': user.email,
                        'domain': current_site.domain,
                        'site_name': 'Finum',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, parameters)
                    try:
                        send_mail(subject, email, 'hello@finum.online', [user.email], fail_silently=False)
                    except:
                        return HttpResponse('Invalid Header')
                    return redirect('password_reset_done')
            else:
                password_form.errors['email_404'] = 'Email not found'
    else:
        password_form = PasswordResetForm()

    context = {
        'password': password_form
    }

    return render(request, 'registration/password_reset_form.html', context)


@login_required(login_url='/signin/')
def deactivate_user(request):
    user = request.user
    user.is_active = False
    user.save()
    return redirect('dashboard:dashboard')


def email_invalid(request):
    return render(request, 'registration/email_send_invalid.html')


def email_send_success(request):
    return render(request, 'registration/email_send_success.html')


def bad_request(request):
    return render(request, 'registration/bad_request.html')
