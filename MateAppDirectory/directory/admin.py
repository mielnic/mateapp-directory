from django.contrib import admin
from .models import Person, Address, Company, Lead
from unfold.admin import ModelAdmin

# Register your models here.

@admin.register(Person)
class CustomAdminClass(ModelAdmin):
    pass

@admin.register(Address)
class CustomAdminClass(ModelAdmin):
    pass

@admin.register(Company)
class CustomAdminClass(ModelAdmin):
    pass

@admin.register(Lead)
class CustomAdminClass(ModelAdmin):
    pass