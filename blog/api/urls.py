from django.urls import path
from blog.api.views import post_list, post_detail, ApiBlogListView

app_name = 'blog'

urlpatterns = [
    path('', post_list, name='blog-home'),
    path('post/<int:pk>/', post_detail, name='post-detail'),
    path('list/', ApiBlogListView.as_view(), name='list')
]