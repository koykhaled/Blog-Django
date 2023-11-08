from django.shortcuts import render , redirect
from django.http import HttpResponse , Http404
from django.shortcuts import get_object_or_404

from .models import Post , Comments
from django.contrib.auth.models import User
from .forms import EmailPostForm  , CommentsForm ,SearchForm

from taggit.models import Tag
from django.db.models import Count

from django.core.paginator import Paginator , EmptyPage,PageNotAnInteger
from django.core.mail import send_mail
from django.conf import settings

from django.contrib.postgres.search import SearchVector,SearchQuery,SearchRank

# Create your views here.
def posts(request,tag_slug=None):
    try:
        post_list = Post.published.all()
        tag = None
        if tag_slug:
            tag = get_object_or_404(Tag,slug=tag_slug)
            post_list = post_list.filter(tags__in=[tag])
        paginator = Paginator(post_list, 2)
        page_number = request.GET.get('page', 1)
        posts = paginator.page(page_number)
    except EmptyPage :
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger :
        posts = paginator.page(1)
    return render(request,'blog/post/posts_list.html',{'posts':posts,'tag':tag})

def post(request,post):
    post = get_object_or_404(Post,slug=post)
    comments = Comments.objects.filter(active=True,post=post)
    
    form = CommentsForm()
    
    # Similiar Posts
    post_id_tags = post.tags.values_list('id',flat=True)
    similar_posts = Post.published.filter(tags__in=post_id_tags).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')
    
    return render(request,'blog/post/post_detail.html',{'post':post,'similar_posts':similar_posts,'comments':comments,'form':form})



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


def post_comments(request,post):
    user = User.objects.get(id=1)
    post = get_object_or_404(Post,slug=post)
    comment = None
    if request.method == "POST":
        form = CommentsForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = user
            comment.save()
            
    else:
        form = CommentsForm()
    return render(request,'blog/post/comment.html',{'form' : form,'post':post,'comment':comment})




def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title','body')
            search_query = SearchQuery(query)
            
            results = Post.published.annotate(
                search=search_vector,
                rank = SearchRank(search_vector,search_query)
            ).filter(search=search_query).order_by('-rank')
    return render(request,'blog/post/search.html',{'form':form,'results':results,'query':query})