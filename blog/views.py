from django.shortcuts import render, get_object_or_404, redirect
from users.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from . models import Post
from django.core.paginator import Paginator
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView
)

# def home(request):
#     context = {
#         'posts': 
#         Post.objects.all()
#     }
#     return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts' #by defautl the variable is called 'objectlist' in template
    ordering = ['-date_posted']
    paginate_by = 10

#authenticate so that only members can view
class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/user_posts.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts' #by defautl the variable is called 'objectlist' in template
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

#authenticate so that only members can view
class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

def search_post(request):
    if request.method == "POST":
        searched = request.POST['searched']
        posts = Post.objects.filter(title__contains=searched).distinct().order_by('-date_posted')
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'blog/search_post.html', {'page_obj':page_obj})