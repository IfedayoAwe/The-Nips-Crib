from django.urls import path
from blog.api.views import new_post, post_detail, ApiBlogListView

app_name = 'blog'

urlpatterns = [
    path('post/<int:pk>/', post_detail, name='post-detail'),
    path('post/', new_post, name='post'),
    path('', ApiBlogListView.as_view(), name='list')
]