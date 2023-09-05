from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, QueryDict, HttpResponse
from django.template import loader
from .forms import PostCreationForm, UploadFileForm, PostEditForm
from django.contrib.auth import get_user_model
from .models import Post, File
from django.db.models.functions import TruncDate
from django.db.models import Value

def post_create(request):
    uid = request.user.id
    user = get_user_model().objects.get(id=uid)
    if request.method == 'POST':
        postcreationform = PostCreationForm(request.POST)
        if postcreationform.is_valid():
            post = postcreationform.save(commit=False)
            post.user = user
            post.save()
            id = post.id
            return HttpResponseRedirect(reverse_lazy("posts:view", kwargs={'id':id}))
    else:
        postcreationform = PostCreationForm()

    context = {
        'postcreationform' : postcreationform,
    }
    return render(request, 'posts/partials/post_create.html', context)

def post_view(request, id):
    post = Post.objects.get(id=id)

    context = {
        'post' : post,
    }
    return render(request, 'posts/view_post.html', context)

def posts_list(request):
    posts_list = Post.objects.order_by('-modified_date').filter(deleted=False).annotate(date=TruncDate('create_date'))
    context = {
        'posts_list' : posts_list
    }
    return render(request, 'posts/list_posts.html', context)

def post_post(request, id):
    '''Esta vista de la de display del partial del contenido del post en htmx'''
    post = Post.objects.get(id=id)
    context = {
        'post' : post,
    }
    return render(request, 'posts/partials/post_post.html', context)

def post_title(request, id):
    '''Esta vista de la de display del partial del contenido del título del post en htmx'''
    post = Post.objects.get(id=id)
    context = {
        'post' : post,
    }
    return render(request, 'posts/partials/post_title.html', context)

def post_edit(request, id):
    '''Edición de post en htmx'''
    post = Post.objects.get(id=id)
    
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
    }
    return render(request, 'posts/partials/post_edit.html', context)

def post_action(request, id):
    post = Post.objects.get(id=id)
    if post.action:
        post.action = False
        post.save()
        return HttpResponse(f'<span hx-get="/posts/post_action/{id}/" hx-swap="outerHTML" hx-target="this"><i class="bi bi-star h5 hx-pointer text-primary me-4"></i></span>')
    else:
        post.action = True
        post.save()
        return HttpResponse(f'<span hx-get="/posts/post_action/{id}/" hx-swap="outerHTML" hx-target="this"><i class="bi bi-star-fill h5 hx-pointer text-primary me-4"></i></span>')

def post_delete(request, id):
    post = Post.objects.get(id=id)
    uid = request.user.id
    post.deleted = True
    post.deletedBy = uid
    post.save()
    return HttpResponse(status = 200)

def post_restore(request, id):
    post = Post.objects.get(id=id)
    post.deleted = False
    post.save()
    return HttpResponse(status = 200)

def post_full_delete(request, id):
    post = Post.objects.get(id=id)
    post.deletedBy = None
    post.save()
    return HttpResponse(status = 200)

def file_upload(request):
    if request.method == 'POST':
        uploadfileform = UploadFileForm(request.POST, request.FILES)
        file = request.FILES['file']
    else:
        uploadfileform = UploadFileForm()

    context = {
        'uploadfileform': uploadfileform,
    }
    return render(request, 'docs/upload.html', context)