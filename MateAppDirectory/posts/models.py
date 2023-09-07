from django.db import models
from django.conf import settings

from directory.models import Person, Company

class BaseModel(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(blank=True, default=0)
    deletedBy = models.BigIntegerField(blank=True, null=True)
    
    class Meta:
        abstract = True

class Post(BaseModel):
    post = models.TextField(max_length=2000, blank=True, null=True)
    action = models.BooleanField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True)
    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, blank=True, null=True)
    post_title = models.CharField(max_length=200, blank=True, null=True)
    
    def title(self):
        title = self.post.split('\n', 1)[0]
        return title

    def save(self, *args, **kwargs):
        self.post_title = self.title()
        super(Post, self).save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.person} {self.company}: {self.post_title}'

class File(BaseModel):
    name = models.CharField(max_length=200, null=True)
    file = models.FileField(upload_to='posts', null=True)
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING, blank=True, null=True)

