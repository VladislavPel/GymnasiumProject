from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from .models import Post, Tag
from .utils import *
from .forms import TagForm, PostForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from django.db.models import Q

def posts_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
    else:
        posts = Post.objects.all()
    paginator = Paginator(posts, 10)



    page_number = request.GET.get('page', 10)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    context = {
        'page_object': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url

    }


    return render(request, 'qwe/index.html', context=context)

class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'qwe/post_detail.html'

class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model_form = PostForm
    template = 'qwe/post_create_form.html'
    raise_exception = True

class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Post
    model_form = PostForm
    template = 'qwe/post_update_form.html'
    raise_exception = True

class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Post
    template = 'qwe/post_delete_form.html'
    redirect_url = 'posts_list_url'
    raise_exception = True



class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'qwe/tag_detail.html'

class TagCreate(LoginRequiredMixin, ObjectDeleteMixin, View):
    model_form = TagForm
    template = 'qwe/tag_create.html'
    raise_exception = True

class TagUpdate(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Tag
    model_form = TagForm
    template = 'qwe/tag_update_form.html'
    raise_exception = True

class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Tag
    template = 'qwe/tag_delete_form.html'
    redirect_url = 'tags_list_url'
    raise_exception = True



def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'qwe/tags_list.html', context={'tags': tags})


