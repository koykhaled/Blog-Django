from django.urls import path
from .views import posts , post , post_share , post_comments
app_name = 'blog'
urlpatterns = [
    path('/',posts,name='posts'),
    path('/tag/<slug:tag_slug>',posts,name='post_by_tags'),
    path('/<slug:post>',post,name='post'),
    path('/<int:post_id>/share',post_share,name='share'),
    path('/<slug:post>/comments',post_comments,name='comments')
]
