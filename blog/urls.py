from django.urls import path
from .views import posts , post
app_name = 'blog'
urlpatterns = [
    path('/',posts,name='posts'),
    path('/<slug:post>',post,name='post'),
]
