from django.urls import path
from .views import posts , post , post_share , post_comments
from django.contrib.sitemaps.views import sitemap
from .sitemaps import PostSitemap
app_name = 'blog'

sitemaps = {
    'posts' : PostSitemap
}
urlpatterns = [
    path('/',posts,name='posts'),
    path('/tag/<slug:tag_slug>',posts,name='post_by_tags'),
    path('/<slug:post>',post,name='post'),
    path('/<int:post_id>/share',post_share,name='share'),
    path('/<slug:post>/comments',post_comments,name='comments'),
    path('/sitemap.xml', sitemap, {'sitemaps': sitemaps},
    name='django.contrib.sitemaps.views.sitemap')
]
