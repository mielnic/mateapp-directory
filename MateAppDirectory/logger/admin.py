from django.contrib import admin
from .models import LogFileProxy
from django.urls import path
from django.template.response import TemplateResponse
from .utils import get_log_file_content

@admin.register(LogFileProxy)
class LogFileProxyAdmin(admin.ModelAdmin):
    change_list_template = "admin/logfile_change_list.html"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', self.admin_site.admin_view(self.view_logfile), name='ovd_logfileproxy_changelist'),
        ]
        return custom_urls + urls
    
    def get_queryset(self, request):
        # Return an empty queryset to prevent database queries
        return LogFileProxy.objects.none()

    def view_logfile(self, request):
        # Include logic to get your log contents
        context = dict(
           self.admin_site.each_context(request),
           log_file_content=get_log_file_content(),
        )
        return TemplateResponse(request, "admin/logfile.html", context)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser
