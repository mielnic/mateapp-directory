from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, response, request
from .forms import CustomUserCreationForm, CustomUserChangeForm, ChangePasswordForm, PasswordResetForm
from main.decorators import user_not_authenticated, allowed_users
from .models import CustomUser
from .managers import CustomUserManager
from main.functions import paginator
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template import loader
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.db.models.query_utils import Q

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
        'user': user.first_name,
        'domain': get_current_site(request).domain,
        'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
        'token' : account_activation_token.make_token(user),
        'protocol' : 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    try:
        email.send()
        messages.success(request, f'Dear <b>{user}</b>, please go to your email inbox and click on \
                     the included activation link to enable your account. <b>Note:</b> Remember to check your spam folder.')
    except:
        user.delete()
        messages.error(request, f'There was a problem sending the email. Please contact the Administrator')    

# Handles registration form.

@user_not_authenticated
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

# Profile View

@login_required
def profileView(request):
    id = request.user.id
    user = get_user_model().objects.get(id=id)
    template = loader.get_template('users/profile.html')
    context = {
        'user' : user,
    }
    return HttpResponse(template.render(context, request))

# Profile Edit

@login_required
def profileEdit(request):
    id = request.user.id
    user = get_user_model().objects.get(id=id)
    profileform = CustomUserChangeForm(request.POST or None, instance = user)
    if profileform.is_valid():
        profileform.save()
        return HttpResponseRedirect('/users/profile/')
    else:
            for error in profileform.errors.values():
                messages.error(request, error)
    context = {
        'profileform': profileform,
    }
    return render(request, 'users/profile_edit.html', context)

# Password Change

@login_required
def passwordChange(request):
    user = request.user
    if request.method == 'POST':
        changepasswordform = ChangePasswordForm(request.POST, instance=user)
        if changepasswordform.is_valid():
            changepasswordform.save()
            return HttpResponseRedirect('/login/')
        else:
            for error in changepasswordform.errors.values():
                messages.error(request, error)
    else:
        changepasswordform = ChangePasswordForm(instance=user)
    context = {
        'changepasswordform': changepasswordform,
    }
    return render(request, 'users/password_change.html', context)

# Password Reset

@user_not_authenticated
def passwordResetRequest(request):
    if request.method == 'POST':
        passwordresetform = PasswordResetForm(request.POST)
        if passwordresetform.is_valid():
            user_email = passwordresetform.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email = user_email)).first()
            if associated_user:
                mail_subject = 'Password Reset Request'
                message = render_to_string('users/password_reset_email.html', {
                'user': associated_user.first_name,
                'domain': get_current_site(request).domain,
                'uid' : urlsafe_base64_encode(force_bytes(associated_user.pk)),
                'token' : account_activation_token.make_token(associated_user),
                'protocol' : 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(mail_subject, message, to=[associated_user])
                try:
                    email.send()
                    messages.success(request, f'Dear <b>{associated_user}</b>, please go to your email inbox and click on \
                                the included link to reset your password. <b>Note:</b> Remember to check your spam folder.')
                    return redirect('/login/')
                except:
                    messages.error(request, f'There was a problem sending the email. Please contact the Administrator')

            return redirect('/login/')
        
    passwordresetform = PasswordResetForm()
    context = {
        'passwordresetform': passwordresetform,
    }
    return render(request, 'users/password_reset.html', context)


def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        print(user)
        if request.method == 'POST':
            changepasswordform = ChangePasswordForm(request.POST, instance=user)
            if changepasswordform.is_valid():
                changepasswordform.save()
                messages.success(request, "Your password has been set. You may go ahead and <b>log in </b> now.")
                return redirect('/login/')
            else:
                for error in list(changepasswordform.errors.values()):
                    messages.error(request, error)

        changepasswordform = ChangePasswordForm(instance=user)
        return render(request, 'users/password_change.html', {'changepasswordform': changepasswordform})
    else:
        messages.error(request, "Link is expired")

    messages.error(request, 'Something went wrong, redirecting back to Homepage')
    return redirect("/login/")

# Users list (Admin)

@login_required
@allowed_users(allowed_roles=['admin'])
def users(request, a=0, b=10):
    users_list = get_user_model().objects.order_by('last_name') [a:b]
    length = get_user_model().objects.count()
    links, idxPL, idxPR, idxNL, idxNR = paginator(a, length, 10)
    template = loader.get_template('users/users.html')
    context = {
        'users_list': users_list,
        'links' : links,
        'idxPL' : idxPL,
        'idxPR' : idxPR,
        'idxNL' : idxNL,
        'idxNR' : idxNR,
    }
    return HttpResponse(template.render(context, request))

# User profile view (Admin)

@login_required
@allowed_users(allowed_roles=['admin'])
def user(request, id):
    muser = get_user_model().objects.get(id=id)
    template = loader.get_template('users/user.html')
    context = {
        'muser' : muser,
    }
    return HttpResponse(template.render(context, request))

