from django.urls import path
from .views import posts , post , post_share
app_name = 'blog'
urlpatterns = [
    path('/',posts,name='posts'),
    path('/<slug:post>',post,name='post'),
    path('/<int:post_id>/share',post_share,name='share')
]
