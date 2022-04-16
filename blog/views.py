from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404
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
)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts' #by defautl the variable is called 'objectlist' in template
    ordering = ['-date_posted']
    paginate_by = 10

class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts' #by defautl the variable is called 'objectlist' in template
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

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

    if not request.method == 'POST':
        if 'searched' in request.session:
            request.POST = request.session['searched']
            request.method = 'POST'

    if request.method == "POST":
        searched = request.POST['searched']

        if searched == '':
            return redirect('blog-home')

        request.session['searched'] = request.POST
        result_list = Post.objects.filter(
                                        Q(title__contains=searched) | 
                                        Q(content__contains=searched) | 
                                        Q(author__username__contains=searched)
                                        ).distinct().order_by('-date_posted')
        paginator = Paginator(result_list, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    else:
        page_obj = ()
    return render(request,  'blog/search_post.html', {'page_obj':page_obj, 'searched':searched})