from django.db import models

class LogFileProxy(models.Model):
    class Meta:
        verbose_name = 'Log File'
        verbose_name_plural = 'Log Files'
        managed = False
        default_permissions = ()