from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, response, request, QueryDict
from django.template import loader
from django.contrib import messages
from .models import Address, Company, Person
from main.functions import paginator
from main.forms import SearchForm
from .forms import PersonForm, CompanyForm, AddressFrom, PersonNotesForm, CompanyNotesForm
from django.contrib.auth.decorators import login_required, permission_required
import copy
from django.utils.translation import gettext_lazy as _
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

# Persons List

@login_required
def persons(request, a, b):
    searchform = SearchForm
    if 'q' in request.GET:
        searchform = SearchForm(request.GET)
        if searchform.is_valid():
            q = searchform.cleaned_data['q']
            ln_list = Person.objects.filter(lastName__icontains=q, deleted=False)
            fn_list = Person.objects.filter(firstName__icontains=q, deleted=False)
            cn_list = Person.objects.filter(company__companyName__icontains=q, deleted=False)
            person_list = sorted(chain(ln_list, fn_list, cn_list),
                             key=attrgetter('lastName'),
                             )
            links, idxPL, idxPR, idxNL, idxNR = '', '', '', '', ''
            template = loader.get_template('directory/persons.html')
            if not person_list:
                messages.warning(request, _("The search didn't return any result."))
    else:
        person_list = Person.objects.order_by('lastName').select_related('company').filter(deleted=False) [a:b]
        length = Person.objects.filter(deleted=False).count()
        links, idxPL, idxPR, idxNL, idxNR = paginator(a, length, b)
        template = loader.get_template('directory/persons.html')
    context = {
        'person_list': person_list,
        'searchform' : searchform,
        'links' : links,
        'idxPL' : idxPL,
        'idxPR' : idxPR,
        'idxNL' : idxNL,
        'idxNR' : idxNR,
    }
    return HttpResponse(template.render(context, request))

# Companies List

@login_required
def companies(request, a, b):
    searchform = SearchForm
    if 'q' in request.GET:
        searchform = SearchForm(request.GET)
        if searchform.is_valid():
            q = searchform.cleaned_data['q']
            companies_list = Company.objects.filter(companyName__icontains=q, deleted=False)
            links, idxPL, idxPR, idxNL, idxNR = '', '', '', '', ''
            template = loader.get_template('directory/companies.html')
            if not companies_list:
                messages.warning(request, _("The search didn't return any result."))

    else:
        companies_list = Company.objects.order_by('companyName').select_related('address').filter(deleted=False) [a:b]
        length = Company.objects.filter(deleted=False).count()
        links, idxPL, idxPR, idxNL, idxNR = paginator(a, length, b)
        template = loader.get_template('directory/companies.html')

    context = {
        'companies_list': companies_list,
        'searchform' : searchform,
        'links' : links,
        'idxPL' : idxPL,
        'idxPR' : idxPR,
        'idxNL' : idxNL,
        'idxNR' : idxNR,
    }
    return HttpResponse(template.render(context, request))

# Person View

@login_required
def person(request, id):
    person = Person.objects.get(id=id)
    template = loader.get_template('directory/person.html')
    context = {
        'person' : person,
    }
    return HttpResponse(template.render(context, request))

# Company View

@login_required
def company(request, id, a, b):
    company = Company.objects.get(id=id)
    person_list = Person.objects.filter(company_id=id).filter(deleted=False) [a:b]
    length = Person.objects.filter(company_id=id).filter(deleted=False).count()
    links, idxPL, idxPR, idxNL, idxNR = paginator(a, length, b)
    template = loader.get_template('directory/company.html')
    context = {
        'company' : company,
        'person_list' : person_list,
        'links' : links,
        'idxPL' : idxPL,
        'idxPR' : idxPR,
        'idxNL' : idxNL,
        'idxNR' : idxNR,
    }
    return HttpResponse(template.render(context, request))

################################
# CREATE, UPDATE, DELETE Views #
################################

# Person Create

@login_required
def create_person(request):
    print(request)
    if request.method == 'POST':
        if '100' in request.POST:
            personform = PersonForm(request.POST)
            addressform = AddressFrom(request.POST)
            companyform = CompanyForm(request.POST)
            if personform.is_valid():
                personform.save()
                id = Person.objects.last().id
                return HttpResponseRedirect(f'/directory/person/{id}/')
        
        elif '110' in request.POST:
            personform = PersonForm(request.POST)
            addressform = AddressFrom(request.POST)
            companyform = CompanyForm(request.POST) 
            if personform.is_valid() and addressform.is_valid():
                addressform.save()
                aid = Address.objects.last().id
                personform.save()
                id = Person.objects.last().id
                person = Person.objects.get(id=id)
                person.address_id = aid
                person.save()
                return HttpResponseRedirect(f'/directory/person/{id}/')

        elif '111' in request.POST:
            personform = PersonForm(request.POST)
            addressform = AddressFrom(request.POST)
            companyform = CompanyForm(request.POST)
            if personform.is_valid() and addressform.is_valid():
                addressform.save()
                aid = Address.objects.last().id
                personform.save()
                id = Person.objects.last().id
                person = Person.objects.get(id=id)
                person.address_id = aid
                person.save()

                return HttpResponseRedirect(f'/directory/person/{id}/')


        elif '112' in request.POST:
            personform = PersonForm(request.POST)
            addressform = AddressFrom(request.POST)
            companyform = CompanyForm(request.POST)
            if personform.is_valid() and addressform.is_valid() and companyform.is_valid():
                addressform_company = copy.deepcopy(addressform)
                addressform.save()
                aid = Address.objects.last().id
                addressform_company.save()
                caid = Address.objects.last().id
                personform.save()
                pid = Person.objects.last().id
                companyform.save()
                cid = Company.objects.last().id
                
                person = Person.objects.get(id=pid)
                person.company_id = cid
                person.address_id = aid
                person.save()
               
                company = Company.objects.get(id=cid)
                company.address_id = caid
                company.save()

                return HttpResponseRedirect(f'/directory/person/{pid}/')
        
        elif '102' in request.POST:
            personform = PersonForm(request.POST)
            addressform = AddressFrom(request.POST)
            companyform = CompanyForm(request.POST)
            if personform.is_valid() and companyform.is_valid():
                personform.save()
                pid = Person.objects.last().id
                companyform.save()
                cid = Company.objects.last().id
                
                person = Person.objects.get(id=pid)
                person.company_id = cid
                person.save()

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
            addressform.save()
            aid = Address.objects.last().id
            personform.save()
            person.address_id = aid
            person.save()
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
    if u == 0:
        return redirect('/user_trash/0/10/')
    else:
        return redirect('/admin_trash/0/10/')

# Person Full Delete

@login_required
def full_delete_person(request, id):
    person = Person.objects.get(id=id)
    person.deletedBy = None
    person.save()
    return redirect('/user_trash/0/10/')


# Company Create

@login_required
def create_company(request):
    if request.method == 'POST':
        companyform = CompanyForm(request.POST)
        addressform = AddressFrom(request.POST)
        if companyform.is_valid() and addressform.is_valid():
            addressform.save()
            aid = Address.objects.last().id
            companyform.save()
            id = Company.objects.last().id
            company = Company.objects.get(id=id)
            company.address_id = aid
            company.save()
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
            addressform.save()
            aid = Address.objects.last().id
            companyform.save()
            company.address_id = aid
            company.save()
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
    if u == 0:
        return redirect('/user_trash/0/10/')
    else:
        return redirect('/admin_trash/0/10/')

# Company Full Delete

@login_required
def full_delete_company(request, id):
    company = Company.objects.get(id=id)
    company.deletedBy = None
    company.save()
    return redirect('/user_trash/0/10/')

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