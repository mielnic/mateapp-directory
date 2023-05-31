from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, response, request
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout, authenticate, get_user_model
from .decorators import user_not_authenticated
from .forms import SearchForm
from django.contrib.auth.decorators import login_required
from directory.models import Person, Company, Address
from itertools import chain
from operator import attrgetter
from django.contrib.postgres.search import TrigramSimilarity



# Create your views here.

def home(request):
    return render(request,'main/home.html')

# Login

@user_not_authenticated
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

# Search

@login_required
def search(request):
    searchform = SearchForm
    results = ''

    if 'q' in request.GET:
        searchform = SearchForm(request.GET)
        if searchform.is_valid():
            q = searchform.cleaned_data['q']
            ln_results = Person.objects.annotate(similarity=TrigramSimilarity('lastName', q),).filter(similarity__gte=0.3).order_by('-similarity')
            fn_results = Person.objects.annotate(similarity=TrigramSimilarity('firstName', q),).filter(similarity__gte=0.3).order_by('-similarity')
            c_results = Company.objects.annotate(similarity=TrigramSimilarity('companyName', q),).filter(similarity__gte=0.3).order_by('-similarity')
            results = sorted(chain(ln_results, fn_results, c_results),
                             key=attrgetter('similarity'),
                             reverse=True,
                             )

        else:
            results = ''

    context = {
        'searchform' : searchform,
        'results' : results,
    }

    return render(request, 'main/home.html', context)