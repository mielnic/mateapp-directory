from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, response, request, QueryDict
from django.template import loader
from django.contrib import messages
from django.db.models.functions import TruncDate
from django.contrib.auth import get_user_model
from django.db.models import Q, Value, Count, Min
from django.core.paginator import Paginator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse_lazy
from .models import Address, Company, Person, Favorite
from posts.models import Post
from main.functions import paginator
from main.forms import SearchForm
from posts.forms import PostCreationForm
from .forms import PersonForm, CompanyForm, AddressFrom, PersonNotesForm, CompanyNotesForm
import copy
from itertools import chain
from operator import attrgetter


########
# MAIN #
########

# Index

@login_required
def index(response):
    return redirect('/directory/persons/0/10/')


##############
# READ Views #
##############

# Fav List

@login_required
def favs(request):
    uid = request.user.id
    user = get_user_model().objects.get(id=uid)
    person_list = Person.objects.filter(Q(favorite__user=user, deleted=False)).annotate(entity=Value('lastName')).annotate(is_person=Value(True)).annotate(fav_id=Min('favorite__id', filter=Q(favorite__user=user)))
    companies_list = Company.objects.filter(Q(favorite__user=user, deleted=False)).annotate(entity=Value('companyName')).annotate(is_person=Value(False)).annotate(fav_id=Min('favorite__id', filter=Q(favorite__user=user)))
    fav_list = sorted(chain(person_list, companies_list),
                      key=attrgetter('entity'),
                      reverse=False,
                      )
    context = {
        'fav_list' : fav_list,
    }
    return render(request, 'directory/favs.html', context)

# Persons List

@login_required
def persons(request, a, b):
    uid = request.user.id
    user = get_user_model().objects.get(id=uid)
    searchform = SearchForm
    if 'q' in request.GET:
        searchform = SearchForm(request.GET)
        if searchform.is_valid():
            q = searchform.cleaned_data['q']
            ln_list = Person.objects.filter(lastName__icontains=q, deleted=False).annotate(fav=Count('favorite__user', filter=Q(favorite__user=user)))
            fn_list = Person.objects.filter(firstName__icontains=q, deleted=False).annotate(fav=Count('favorite__user', filter=Q(favorite__user=user)))
            cn_list = Person.objects.filter(company__companyName__icontains=q, deleted=False).annotate(fav=Count('favorite__user', filter=Q(favorite__user=user)))
            person_list = sorted(chain(ln_list, fn_list, cn_list),
                             key=attrgetter('lastName'),
                             )
            pgx = ''
            template = loader.get_template('directory/persons.html')
            if not person_list:
                messages.warning(request, _("The search didn't return any result."))
    else:
        person_list = Person.objects.order_by('lastName').select_related('company').filter(deleted=False).annotate(fav=Count('favorite__user', filter=Q(favorite__user=user)))  [a:b]
        length = Person.objects.filter(deleted=False).count()
        pgx = paginator(a, length, b)
        template = loader.get_template('directory/persons.html')
    context = {
        'person_list': person_list,
        'searchform' : searchform,
        'pgx' : pgx,
    }
    return HttpResponse(template.render(context, request))

# Companies List

@login_required
def companies(request, a, b):
    uid = request.user.id
    user = get_user_model().objects.get(pk=uid)
    searchform = SearchForm
    if 'q' in request.GET:
        searchform = SearchForm(request.GET)
        if searchform.is_valid():
            q = searchform.cleaned_data['q']
            companies_list = Company.objects.filter(companyName__icontains=q, deleted=False).annotate(fav=Count('favorite__user', filter=Q(favorite__user=user))) 
            pgx = ''
            template = loader.get_template('directory/companies.html')
            if not companies_list:
                messages.warning(request, _("The search didn't return any result."))

    else:
        companies_list = Company.objects.order_by('companyName').select_related('address').filter(deleted=False).annotate(fav=Count('favorite__user', filter=Q(favorite__user=user))) [a:b]
        length = Company.objects.filter(deleted=False).count()
        pgx = paginator(a, length, b)
        template = loader.get_template('directory/companies.html')

    context = {
        'companies_list': companies_list,
        'searchform' : searchform,
        'pgx' : pgx,
    }
    return HttpResponse(template.render(context, request))

# Person View

@login_required
def person(request, id):
    uid = request.user.id
    person = Person.objects.get(id=id)
    posts_list = Post.objects.filter(person=person, deleted=False).order_by('-modified_date').annotate(date=TruncDate('create_date'))
    paginator = Paginator(posts_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    try:
        fav = Favorite.objects.get(user = uid, person=person.id)
    except:
        fav = False
    if request.htmx:
        template = loader.get_template('directory/partials/person_posts_list.html')
    else:
        template = loader.get_template('directory/person.html')
    context = {
        'person' : person,
        'fav' : fav,
        'page_obj' : page_obj,
    }
    return HttpResponse(template.render(context, request))

# Company View

@login_required
def company(request, id, a, b):
    uid = request.user.id
    company = Company.objects.get(id=id)
    posts_list = Post.objects.filter(Q(company=company) | Q(person__company=company)).filter(deleted=False).order_by('-modified_date').annotate(date=TruncDate('create_date'))
    paginator = Paginator(posts_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    try:
        fav = Favorite.objects.get(user = uid, company=company.id)
    except:
        fav = False
    person_list = Person.objects.filter(company_id=id).filter(deleted=False)
    if request.htmx:
        template = loader.get_template('directory/partials/company_posts_list.html')
    else:
        template = loader.get_template('directory/company.html')
    context = {
        'company' : company,
        'fav' : fav,
        'person_list' : person_list,
        'page_obj' : page_obj,
    }
    return HttpResponse(template.render(context, request))



################################
# CREATE, UPDATE, DELETE Views #
################################

# Person Create

@login_required
def create_person(request):
    if request.method == 'POST':
        if '100' in request.POST:
            personform = PersonForm(request.POST)
            addressform = AddressFrom(request.POST)
            companyform = CompanyForm(request.POST)
            if personform.is_valid():
                person = personform.save()
                id = person.id
                return HttpResponseRedirect(f'/directory/person/{id}/')
        
        elif '110' in request.POST:
            personform = PersonForm(request.POST)
            addressform = AddressFrom(request.POST)
            companyform = CompanyForm(request.POST) 
            if personform.is_valid() and addressform.is_valid():
                address = addressform.save()
                person = personform.save(commit=False)
                person.address = address
                person.save()
                id = person.id
                return HttpResponseRedirect(f'/directory/person/{id}/')

        elif '111' in request.POST:
            personform = PersonForm(request.POST)
            addressform = AddressFrom(request.POST)
            companyform = CompanyForm(request.POST)
            if personform.is_valid() and addressform.is_valid():
                address = addressform.save()
                personform.save(commit=False)
                person.address = address
                person.save()
                id = person.id
                return HttpResponseRedirect(f'/directory/person/{id}/')


        elif '112' in request.POST:
            personform = PersonForm(request.POST)
            addressform = AddressFrom(request.POST)
            companyform = CompanyForm(request.POST)
            if personform.is_valid() and addressform.is_valid() and companyform.is_valid():
                addressform_company = copy.deepcopy(addressform)
                paddress = addressform.save()
                caddress = addressform_company.save()
                person = personform.save(commit=False)
                company = companyform.save(commit=False)
                
                company.address = caddress
                company.save()

                person.company = company
                person.address = paddress
                person.save()
                pid = person.id

                return HttpResponseRedirect(f'/directory/person/{pid}/')
        
        elif '102' in request.POST:
            personform = PersonForm(request.POST)
            addressform = AddressFrom(request.POST)
            companyform = CompanyForm(request.POST)
            if personform.is_valid() and companyform.is_valid():
                person = personform.save(commit=False)
                company = companyform.save()

                person.company = company
                person.save()
                pid = person.id
                return HttpResponseRedirect(f'/directory/person/{pid}/')

    else:
        companyform = CompanyForm()
        personform = PersonForm()
        addressform =  AddressFrom()

    context = {
        'companyform' : companyform,
        'personform': personform,
        'addressform' : addressform,
        'title': _("New Person")
    }
    return render(request, 'directory/create_person.html', context)

# Person Update

@login_required
def edit_person(request, id):
    person = Person.objects.get(id=id)
    try:
        paid = person.address.id
        address = Address.objects.get(id=paid)
        personform = PersonForm(request.POST or None, instance=person)
        addressform = AddressFrom(request.POST or None, instance=address)
        if personform.is_valid() and addressform.is_valid():
            addressform.save()
            personform.save()
            person.address_id = paid
            person.save()
            return HttpResponseRedirect(f'/directory/person/{id}/')
    except:
        personform = PersonForm(request.POST or None, instance=person)
        addressform = AddressFrom(request.POST or None)
        if personform.is_valid() and addressform.is_valid():
            address = addressform.save()
            person = personform.save(commit=False)
            person.address = address
            person.save()
            id = person.id
            return HttpResponseRedirect(f'/directory/person/{id}/')
    
    context = {
        'personform': personform,
        'addressform' : addressform,
        'person' : person,
    }
    return render(request, 'directory/create_person.html', context)

# Person Delete

@login_required
def delete_person(request, id):
    uid = request.user.id
    person = Person.objects.get(id=id)
    person.deleted = 1
    person.deletedBy = uid
    person.save()
    return redirect('/directory/persons/0/10/')

# Person Restore

@login_required
def restore_person(request, id, u):
    person = Person.objects.get(id=id)
    person.deleted = 0
    person.save()
    return HttpResponse(status = 200)

# Person Full Delete

@login_required
def full_delete_person(request, id):
    person = Person.objects.get(id=id)
    person.deletedBy = None
    person.save()
    return HttpResponse(status = 200)


# Company Create

@login_required
def create_company(request):
    if request.method == 'POST':
        companyform = CompanyForm(request.POST)
        addressform = AddressFrom(request.POST)
        if companyform.is_valid() and addressform.is_valid():
            address = addressform.save()
            company = companyform.save(commit=False)
            company.address = address
            company.save()
            id = company.id
            return HttpResponseRedirect(f'/directory/company/{id}/0/5/')     

    else:
        companyform = CompanyForm()
        addressform = AddressFrom()

    context = {
        'companyform': companyform,
        'addressform' : addressform,
        'title': _("New Company")
    }
    return render(request, 'directory/create_company.html', context)

# Company Update

@login_required
def edit_company(request, id):
    company = Company.objects.get(id=id)
    try:
        caid = company.address.id
        address = Address.objects.get(id=caid)
        addressform = AddressFrom(request.POST or None, instance=address)
        companyform = CompanyForm(request.POST or None, instance=company)
        if companyform.is_valid() and addressform.is_valid():
            addressform.save()
            companyform.save()
            company.address_id = caid
            company.save()
            return HttpResponseRedirect(f'/directory/company/{id}/0/5/')
    except:
        addressform = AddressFrom(request.POST or None)
        companyform = CompanyForm(request.POST or None, instance=company)
        if companyform.is_valid() and addressform.is_valid():
            address = addressform.save()
            company = companyform.save(commit=False)
            company.address = address
            company.save()
            id = company.id
            return HttpResponseRedirect(f'/directory/company/{id}/0/5/')
    
    context = {
        'companyform': companyform,
        'addressform': addressform,
        'company' : company,
    }
    return render(request, 'directory/create_company.html', context)

# Company Delete

@login_required
def delete_company(request, id):
    uid = request.user.id
    company = Company.objects.get(id=id)
    company.deleted = 1
    company.deletedBy = uid
    company.save()
    return redirect('/directory/companies/0/10/')

# Company Restore

@login_required
def restore_company(request, id, u):
    company = Company.objects.get(id=id)
    company.deleted = 0
    company.save()
    return HttpResponse(status = 200)

# Company Full Delete

@login_required
def full_delete_company(request, id):
    company = Company.objects.get(id=id)
    company.deletedBy = None
    company.save()
    return HttpResponse(status = 200)

#############
# Favorites #
#############

@login_required
def link_favorite(request, obj, oid):
    uid = request.user.id
    user = get_user_model().objects.get(pk=uid)
    if obj == 'person_obj':
        person = Person.objects.get(id=oid)
        favorite = Favorite(user=user, person=person)
        favorite.save()
    else:
        company = Company.objects.get(id=oid)
        favorite = Favorite(user=user, company=company)
        favorite.save()
    return HttpResponse(f'<span class="px-2" hx-get="/directory/unlink_fav/{ favorite.id }/" hx-swap="outerHTML"><i class="bi bi-star-fill h5 hx-pointer text-warning"></i></span>')

@login_required
def unlink_favorite(request, lid):
    try:
        pid = Favorite.objects.get(id=lid).person.id
        Favorite.objects.filter(id=lid).delete()
        return HttpResponse(f'<span class="px-2" hx-get="/directory/link_fav/person_obj/{ pid }/" hx-swap="outerHTML"><i class="bi bi-star h5 hx-pointer text-warning"></i></span>')
    except:
        pid = Favorite.objects.get(id=lid).company.id
        Favorite.objects.filter(id=lid).delete()
        return HttpResponse(f'<span class="px-2" hx-get="/directory/link_fav/company_obj/{ pid }/" hx-swap="outerHTML"><i class="bi bi-star h5 hx-pointer text-warning"></i></span>')

@login_required
def unlink_favorite_favs(request, lid):
    Favorite.objects.filter(id=lid).delete()
    return HttpResponse(status = 200)

##############
# htmx Views #
##############

# Person Notes

@login_required
def personNotes(request, id):
    '''Esta vista de la de display del partial de person notes de htmx'''
    person = Person.objects.get(id=id)
    context = {
        'person' : person,
    }
    return render(request, 'directory/partials/person_notes.html', context)

@login_required
def personNotesTitle(request, id):
    '''Esta vista de la de display del partial de person notes title de htmx'''
    person = Person.objects.get(id=id)
    context = {
        'person' : person,
    }
    return render(request, 'directory/partials/person_notes_title.html', context)

@login_required
def personPostCreate(request, id):
    uid = request.user.id
    user = get_user_model().objects.get(id=uid)
    person = Person.objects.get(id=id)
    if request.method == 'PUT':
        data = QueryDict(request.body).dict()
        postcreationform = PostCreationForm(data)
        if postcreationform.is_valid():
            post = postcreationform.save(commit=False)
            post.user = user
            post.person = person
            post.save()
            return HttpResponseRedirect(reverse_lazy("directory:Person", args=[id]))
    else:
        postcreationform = PostCreationForm()

    context = {
        'postcreationform' : postcreationform,
        'person' : person
    }
    return render(request, 'directory/partials/person_post_create.html', context)

@login_required
def personNotesEdit(request, id):
    '''Esta vista es el tramo de edición del partial de person notes de htmx'''
    person = Person.objects.get(id=id)
    if request.method == 'PUT':
        data = QueryDict(request.body).dict()
        notesform = PersonNotesForm(data, instance=person)
        if notesform.is_valid():
            notesform.save()
            context = {
                'notesform' : notesform,
                'person' : person,
            }
            return render(request, 'directory/partials/person_notes.html', context)

    else:
        notesform = PersonNotesForm(instance=person)

    context = {
        'notesform' : notesform,
        'person' : person,
    }
    return render(request, 'directory/partials/edit_person_notes.html', context)


# Company Notes:

@login_required
def companyNotes(request, id):
    '''Esta vista de la de display del partial de company notes de htmx'''
    company = Company.objects.get(id=id)
    context = {
        'company' : company,
    }
    return render(request, 'directory/partials/company_notes.html', context)

@login_required
def companyNotesTitle(request, id):
    '''Esta vista de la de display del partial de company notes title de htmx'''
    company = Company.objects.get(id=id)
    context = {
        'company' : company,
    }
    return render(request, 'directory/partials/company_notes_title.html', context)

@login_required
def companyNotesEdit(request, id):
    '''Esta vista es el tramo de edición del partial de company notes de htmx'''
    company = Company.objects.get(id=id)
    if request.method == 'PUT':
        data = QueryDict(request.body).dict()
        notesform = CompanyNotesForm(data, instance=company)
        if notesform.is_valid():
            notesform.save()
            context = {
                'notesform' : notesform,
                'company' : company,
            }
            return render(request, 'directory/partials/company_notes.html', context)

    else:
        notesform = CompanyNotesForm(instance=company)

    context = {
        'notesform' : notesform,
        'company' : company,
    }
    return render(request, 'directory/partials/edit_company_notes.html', context)

# Company Persons List

@login_required
def companyPersons(request, id, a, b):
    company = Company.objects.get(id=id)
    person_list = Person.objects.filter(company_id=id).filter(deleted=False) [a:b]
    length = Person.objects.filter(company_id=id).filter(deleted=False).count()
    pgx = paginator(a, length, b)
    template = loader.get_template('directory/partials/company_persons_list.html')
    context = {
        'company' : company,
        'person_list' : person_list,
        'pgx' : pgx
    }
    return HttpResponse(template.render(context, request))

@login_required
def companyPersonsCollapsed(request, id):
    company = Company.objects.get(id=id)
    context = {
        'company' : company
    }

    return render(request, 'directory/partials/company_persons_collapsed.html', context)

@login_required
def companyPostCreate(request, id):
    uid = request.user.id
    user = get_user_model().objects.get(id=uid)
    company = Company.objects.get(id=id)
    if request.method == 'PUT':
        data = QueryDict(request.body).dict()
        postcreationform = PostCreationForm(data)
        if postcreationform.is_valid():
            post = postcreationform.save(commit=False)
            post.user = user
            post.company = company
            post.save()
            return HttpResponseRedirect(reverse_lazy("directory:Company", args=[id, 0, 5]))
    else:
        postcreationform = PostCreationForm()

    context = {
        'postcreationform' : postcreationform,
        'company' : company,
    }
    return render(request, 'directory/partials/company_post_create.html', context)