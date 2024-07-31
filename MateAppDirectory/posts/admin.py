from django.contrib import admin
from .models import Post, File
from unfold.admin import ModelAdmin

# Register your models here.

@admin.register(Post)
class CustomAdminClass(ModelAdmin):
    pass

@admin.register(File)
class CustomAdminClass(ModelAdmin):
    pass