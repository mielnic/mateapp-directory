import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, response, request
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout, authenticate, get_user_model
from .decorators import user_not_authenticated, allowed_users
from .forms import SearchForm
from django.contrib.auth.decorators import login_required
from directory.models import Person, Company, Address
from itertools import chain
from operator import attrgetter
from django.contrib.postgres.search import TrigramSimilarity
from django.utils.translation import gettext_lazy as _
from .functions import paginator
from django.template import loader
from django.core.management import call_command

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
            messages.error(request, _('Incorrect Username or Password.'))
            return render(request, 'main/login.html', {
                'form' : AuthenticationForm,
                'error' : _('Incorrect Username or Password.')
                })
        else:
            auth_login(request, user)
            return redirect('../')

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
            ln_results = Person.objects.annotate(similarity=TrigramSimilarity('lastName', q),).filter(similarity__gte=0.3, deleted=False).order_by('-similarity')
            fn_results = Person.objects.annotate(similarity=TrigramSimilarity('firstName', q),).filter(similarity__gte=0.5, deleted=False).order_by('-similarity')
            pp_results = Person.objects.annotate(similarity=TrigramSimilarity('position', q),).filter(similarity__gte=0.5, deleted=False).order_by('-similarity')
            c_results = Company.objects.annotate(similarity=TrigramSimilarity('companyName', q),).filter(similarity__gte=0.3, deleted=False).order_by('-similarity')
            ct_results = Company.objects.annotate(similarity=TrigramSimilarity('tax_id', q),).filter(similarity__gte=0.6, deleted=False).order_by('-similarity')
            results = sorted(chain(ln_results, fn_results, c_results, pp_results, ct_results),
                             key=attrgetter('similarity'),
                             reverse=True,
                             )
            if results == []:
                print('no results')
                messages.warning(request, _("The search didn't return any result."))

    context = {
        'searchform' : searchform,
        'results' : results,
    }

    return render(request, 'main/home.html', context)

# User Trash

@login_required
def user_trash(request, a, b):
    uid = request.user.id
    deleted_companies_list = Company.objects.filter(deleted=True, deletedBy=uid)
    deleted_person_list = Person.objects.filter(deleted=True, deletedBy=uid)
    trash = list(chain(deleted_person_list, deleted_companies_list))
    length = len(trash)
    links, idxPL, idxPR, idxNL, idxNR = paginator(a, length, 10)
    template = loader.get_template('main/user_trash.html')
    context = {
        'trash_list': trash,
        'links' : links,
        'idxPL' : idxPL,
        'idxPR' : idxPR,
        'idxNL' : idxNL,
        'idxNR' : idxNR,
    }
    return HttpResponse(template.render(context, request))

# Admin Trash

@login_required
@allowed_users(allowed_roles=['admin', 'satff'])
def admin_trash(request, a, b):
    searchform = SearchForm
    if 'q' in request.GET:
        searchform = SearchForm(request.GET)
        if searchform.is_valid():
            q = searchform.cleaned_data['q']
            ln_results = Person.objects.annotate(similarity=TrigramSimilarity('lastName', q),).filter(similarity__gte=0.3, deleted=True).order_by('-similarity')
            fn_results = Person.objects.annotate(similarity=TrigramSimilarity('firstName', q),).filter(similarity__gte=0.5, deleted=True).order_by('-similarity')
            c_results = Company.objects.annotate(similarity=TrigramSimilarity('companyName', q),).filter(similarity__gte=0.3, deleted=True).order_by('-similarity')
            trash = sorted(chain(ln_results, fn_results, c_results),
                             key=attrgetter('similarity'),
                             reverse=True,
                             )
            links, idxPL, idxPR, idxNL, idxNR = '', '', '', '', ''
            template = loader.get_template('main/admin_trash.html')
            if trash == []:
                messages.warning(request, _("The search didn't return any result."))
    else:
        deleted_companies_list = Company.objects.filter(deleted=True)
        deleted_person_list = Person.objects.filter(deleted=True)
        trash = list(chain(deleted_person_list, deleted_companies_list))
        length = len(trash)
        links, idxPL, idxPR, idxNL, idxNR = paginator(a, length, 10)
        template = loader.get_template('main/admin_trash.html')
    
    context = {
        'searchform' : searchform,
        'trash_list': trash,
        'links' : links,
        'idxPL' : idxPL,
        'idxPR' : idxPR,
        'idxNL' : idxNL,
        'idxNR' : idxNR,
    }
    return HttpResponse(template.render(context, request))

# Admin Home (Admin)

@login_required
@allowed_users(allowed_roles=['admin', 'staff'])
def admin_home(request, a=0, b=10):
    # Users List
    users_list = get_user_model().objects.order_by('last_name').filter(is_active=True) [a:b]
    length = get_user_model().objects.filter(is_active=True).count()
    links, idxPL, idxPR, idxNL, idxNR = paginator(a, length, 10)
    # Backup files List
    folder = f'{settings.MEDIA_ROOT}/backup/'
    file_list = os.listdir(folder)
    file_list = file_list[::-1]
    path = f'{settings.MEDIA_URL}backup/'
    template = loader.get_template('main/admin_home.html')
    context = {
        'users_list': users_list,
        'links' : links,
        'idxPL' : idxPL,
        'idxPR' : idxPR,
        'idxNL' : idxNL,
        'idxNR' : idxNR,
        'file_list': file_list,
        'path': path,
    }
    return HttpResponse(template.render(context, request))

@login_required
@allowed_users(allowed_roles=['admin', 'staff'])
def do_backup(request):
    print('hola')
    call_command('dbbackup', clean=True, interactive=False)
    return redirect('/admin_home/0/10/')