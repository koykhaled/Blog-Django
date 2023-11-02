from django.shortcuts import render , redirect
from django.http import HttpResponse , Http404
from .models import Post
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator , EmptyPage,PageNotAnInteger
from .forms import EmailPostForm 
from django.core.mail import send_mail
from django.conf import settings

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



def post_share(request,post_id):
    post = get_object_or_404(Post,id=post_id)
    sent = False
    form = EmailPostForm
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommended you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n {cd['name']}'s {cd['comments']}"
            send_mail(subject,message,settings.EMAIL_HOST_USER,[cd['to']])
            sent = True
        else:
            form = EmailPostForm()
    return render(request,'blog/post/share.html',{'post':post,'form':form,'sent':sent})