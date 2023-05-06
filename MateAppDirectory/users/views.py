from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, response, request
from django.template import loader
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token

# Create your views here.

# Activate

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Thank you for your confirmation. Your account is now active')
        return redirect('/login/')
    else:
        messages.error(request, "Activation link is invalid. Contact the administrator")
    return redirect('/login/')

# Sends Activation Email

def activationEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('users/activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
        'token' : account_activation_token.make_token(user),
        'protocol' : 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to ypur email inbox and click on \
                     the included activation link to enable your account. <b>Note:</b> Remember to check your spam folder.')
    else:
        messages.error(request, f'There was a problem sending the email. Please contact the Amdinistrator')    

# Handles registration form.

def register(request):
    registerform = CustomUserCreationForm(request.POST)
    if request.method == 'POST':  
        if registerform.is_valid():
            user = registerform.save(commit=False)
            user.is_active = False
            user.save()
            activationEmail(request, user, registerform.cleaned_data.get('email'))
            return HttpResponseRedirect('/login/')
        else:
            for error in registerform.errors.values():
                messages.error(request, error)
    
    context = {
        'registerform' : registerform,
    }
    
    return render(request, 'users/registration.html', context)