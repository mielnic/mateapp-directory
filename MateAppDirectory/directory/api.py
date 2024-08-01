from .models import Company, Address, Person, Lead
from rest_framework import viewsets, permissions
from .serializers import CompanySerializer, AddressSerializer, PersonSerializer, LeadSerializer
from rest_framework import viewsets, permissions, mixins, status
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from rest_framework.response import Response

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.filter(deleted=False)
    serializer_class = CompanySerializer

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.filter(deleted=False)
    serializer_class = AddressSerializer

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.filter(deleted=False)
    serializer_class = PersonSerializer

class LeadViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = Lead.objects.filter(deleted=False)
    serializer_class = LeadSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        subject = _('New Web Lead')
        message = render_to_string( 'users/new_web_lead.html', {
            'firstName' : serializer.data['firstName'],
            'lastName' : serializer.data['lastName'],
            'email' : serializer.data['email'],
            'message' : serializer.data['message'],
        })
        email = EmailMessage(subject, message, to=[settings.WEB_TO_LEAD_EMAIL])
        try:
            email.send()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(serializer.data, status=status.HTTP_201_CREATED)