from django.shortcuts import render
from django.http import HttpResponse , Http404
from .models import Post
from django.core.paginator import Paginator , EmptyPage,PageNotAnInteger

# Create your views here.
def posts(request):
    try:
        post_list = Post.published.all()
        paginator = Paginator(post_list, 2)
        page_number = request.GET.get('page', 1)
        posts = paginator.page(page_number)
    except EmptyPage :
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger :
        posts = paginator.page(1)
    return render(request,'blog/post/posts_list.html',{'posts':posts})

def post(request,post):
    try:
        post = Post.published.get(
            slug = post
        )
    except Post.DoesNotExist:
        raise Http404("Post not found")
    
    return render(request,'blog/post/post_detail.html',{'post':post})