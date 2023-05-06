from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, response, request
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout, authenticate, get_user_model



# Create your views here.

# Login

def login(request):
    if request.method == 'GET':
        return render(request, 'main/login.html', {'form' : AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            messages.error(request, 'Incorrect Username or Password')
            return render(request, 'main/login.html', {
                'form' : AuthenticationForm,
                'error' : 'Incorrect Username or Password'
                })
        else:
            auth_login(request, user)
            return redirect('../directory/persons/0/10/')

# Logout

def signout(request):
    logout(request)
    return redirect('/login/')