from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, QueryDict, HttpResponse
from django.template import loader
from .forms import PostCreationForm, UploadFileForm, PostEditForm
from django.contrib.auth import get_user_model
from .models import Post, File
from django.db.models.functions import TruncDate
from django.db.models import Value, Count
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .functions import splitFilename
from django.conf import settings


##############
# Post Views #
##############

# Post Create

@login_required
def post_create(request):
    uid = request.user.id
    user = get_user_model().objects.get(id=uid)
    if request.method == 'PUT':
        data = QueryDict(request.body).dict()
        postcreationform = PostCreationForm(data)
        if postcreationform.is_valid():
            post = postcreationform.save(commit=False)
            post.user = user
            post.save()
            id = post.id
            return HttpResponseRedirect(reverse_lazy("posts:list"))
    else:
        postcreationform = PostCreationForm()

    context = {
        'postcreationform' : postcreationform,
    }
    return render(request, 'posts/partials/post_create.html', context)

# Post View DEPRECATED

@login_required
def post_view(request, id):
    post = Post.objects.get(id=id)

    context = {
        'post' : post,
    }
    return render(request, 'posts/view_post.html', context)

# Post List

@login_required
def posts_list(request):
    posts_list = Post.objects.order_by('-modified_date').filter(deleted=False).annotate(date=TruncDate('create_date'))
    paginator = Paginator(posts_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj' : page_obj
    }
    if request.htmx:
        return render(request, 'posts/partials/posts_list.html', context)
    else:
        return render(request, 'posts/list_posts.html', context)

# Post htmx partial view

@login_required
def post_post(request, id):
    '''Esta vista de la de display del partial del contenido del post en htmx'''
    post = Post.objects.get(id=id)
    files = File.objects.filter(post=post, deleted=False)
    path = f'{settings.MEDIA_URL}'
    context = {
        'post' : post,
        'files' : files,
        'path' : path,
    }
    return render(request, 'posts/partials/post_post.html', context)

# Post htmx collapsed view

@login_required
def post_title(request, id):
    '''Esta vista de la de display del partial del contenido del título del post en htmx'''
    post = Post.objects.get(id=id)
    context = {
        'post' : post,
    }
    return render(request, 'posts/partials/post_title.html', context)

# Post Edit

@login_required
def post_edit(request, id):
    '''Edición de post en htmx'''
    post = Post.objects.get(id=id)
    files = File.objects.filter(post=post, deleted=False)
    path = f'{settings.MEDIA_URL}'
    if request.method == 'PUT':
        data = QueryDict(request.body).dict()
        postform = PostEditForm(data, instance=post)
        if postform.is_valid():
            postform.save()
            context = {
            'postform' : postform,
            'post' : post,
            }
            return render(request, 'posts/partials/post_title.html', context)

    else:
        postform = PostEditForm(instance=post)

    context = {
        'postform' : postform,
        'post' : post,
        'files' : files,
        'path' : path,
    }
    return render(request, 'posts/partials/post_edit.html', context)

# Post htmx action switch

# @login_required
# def post_action(request, id):
#     post = Post.objects.get(id=id)
#     if post.action:
#         post.action = False
#         post.save()
#         return HttpResponse(f'<span hx-get="/posts/post_action/{id}/" hx-swap="outerHTML" hx-target="this"><i class="bi bi-star h5 hx-pointer text-primary me-4"></i></span>')
#     else:
#         post.action = True
#         post.save()
#         return HttpResponse(f'<span hx-get="/posts/post_action/{id}/" hx-swap="outerHTML" hx-target="this"><i class="bi bi-star-fill h5 hx-pointer text-primary me-4"></i></span>')

# Post Delete

@login_required
def post_delete(request, id):
    post = Post.objects.get(id=id)
    uid = request.user.id
    post.deleted = True
    post.deletedBy = uid
    post.save()
    return HttpResponse(status = 200)

# Post Restore

@login_required
def post_restore(request, id):
    post = Post.objects.get(id=id)
    post.deleted = False
    post.save()
    return HttpResponse(status = 200)

# Post Full Delete

@login_required
def post_full_delete(request, id):
    post = Post.objects.get(id=id)
    post.deletedBy = None
    post.save()
    return HttpResponse(status = 200)

##############
# File Views #
##############

def file_upload(request, id):
    post = Post.objects.get(id=id)
    if request.method == 'POST':
        uploadfileform = UploadFileForm(request.POST, request.FILES)
        uploads = request.FILES.getlist('file')
        for upload in uploads:
            file = File.objects.create(file=upload)
            file.post = post
            name=str(upload)
            shortName, color, ext = splitFilename(name)
            file.shortName = shortName
            file.color = color
            file.ext = ext
            file.name = name
            file.save()
        return HttpResponseRedirect(f'/posts/files/{id}/')
    else:
        uploadfileform = UploadFileForm()

    context = {
        'uploadfileform': uploadfileform,
        'post' : post
    }
    return render(request, 'posts/partials/upload.html', context)


def files(request, id):
    post = Post.objects.get(id=id)
    context = {
        'post' : post
    }
    return render(request, 'posts/partials/files.html', context)

def files_list(request, id):
    post = Post.objects.get(id=id)
    files = File.objects.filter(post=post, deleted=False)
    path = f'{settings.MEDIA_URL}'
    context = {
        'post' : post,
        'files' : files,
        'path' : path,
    }
    return render(request, 'posts/partials/files_list.html', context)

def file_delete(request, fid, pid):
    File.objects.filter(id=fid).delete()
    return HttpResponseRedirect(f'/posts/post_edit/{pid}')
    # post = Post.objects.get(id=pid)
    # files = File.objects.filter(post=post, deleted=False)
    # path = f'{settings.MEDIA_URL}'
    # context = {
    #     'post' : post,
    #     'files' : files,
    #     'path' : path,
    # }
    # return render(request, 'posts/partials/post_edit.html', context)

# def files_clip(request, id):
#     post = Post.objects.get(id=id)
#     files = File.objects.filter(post=post, deleted=False)
#     context = {
#         'post' : post,
#         'files' : files,
#     }
#     return render(request, 'posts/partials/files_clip.html', context)