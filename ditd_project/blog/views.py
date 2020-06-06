from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post


class PostListView(ListView): # Home page
    model = Post

    # Changing the default template name
    # default is: # <app>/<model>_<viewtype>.html (ie. blog/post_list.html)
    template_name = 'blog/home.html'

    # changing the name of the returned data
    # Default is called: "object_list"
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

# This is an example of using some non-default settings for class based views
class UserPostListView(ListView):
    model = Post
    # Changing the default template name
    # default is: # <app>/<model>_<viewtype>.html
    template_name = 'blog/user_posts.html'
    # changing the name of the returned data
    # Default is called: "object_list"
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

# This is an example of using all of the default Django conventions for class based views
class PostDetailView(DetailView): 
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    # Here we are overriding the form_valid method that would normally get 
    # run and including a bit to set the author to the current user and
    # then running the form_valid method.
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
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

# This is a function based view
def about(request):
    return render(request, 'blog/about.html', {'title':'About'})