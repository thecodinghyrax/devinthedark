from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from .models import Post
from django.db.models import Q 
from .forms import SearchForm


# Django view takes in a requset and return a response
#                           |                   A
#                           V                   |
#                         URL's  ------------> VIEWS
#                                              -Models
#                                              -Templates


class PostListView(ListView): # Home page
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['newest_post'] = Post.objects.order_by('-date_posted')[0]
        context_data['recent_posts'] = Post.objects.order_by('-date_posted')[1:3]
        context_data['form'] = SearchForm()
        return context_data

    
    queryset = Post.objects.order_by('-date_posted')[3:]

    # # Changing the default template name
    # # default is: # <app>/<model>_<viewtype>.html (ie. blog/post_list.html)
    template_name = 'blog/home.html'

    # # changing the name of the returned data
    # # Default is called: "object_list"
    context_object_name = 'posts'
    # ordering = ['-date_posted']
    paginate_by = 5

# This is an example of using some non-default settings for class based views
class TopicPostListView(ListView):
    model = Post
    # Changing the default template name
    # default is: # <app>/<model>_<viewtype>.html
    template_name = 'blog/topic_posts.html'
    # changing the name of the returned data
    # Default is called: "object_list"
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        topic = self.kwargs.get('topic')
        return Post.objects.filter(topics__topic__contains=topic).order_by('-date_posted')

class SearchPostListView(ListView):
    model = Post
    # Changing the default template name
    # default is: # <app>/<model>_<viewtype>.html
    template_name = 'blog/search_posts.html'
    form_class = SearchForm
    # changing the name of the returned data
    # Default is called: "object_list"
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['word'] = self.request.GET.get('word')
        return context_data

    def get_queryset(self):
        
        word = self.request.GET.get('word')
        return Post.objects.filter(Q(topics__topic__icontains=word) |
                                        Q(content__icontains=word) |
                                        Q(title__icontains=word)).order_by('-date_posted')


# This is an example of using all of the default Django conventions for class based views
class PostDetailView(DetailView): 
    model = Post

    def related_posts(self):
        topic_query = Post.objects.get(pk=self.kwargs.get('pk'))
        try:
            topic = topic_query.get_post_topics()[0][1]
        except:
            topic = "Python"
        return Post.objects.filter(topics__topic__icontains=topic)[0:4]

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'article_image', 'topics']

    # Here we are overriding the form_valid method that would normally get 
    # run and including a bit to set the author to the current user and
    # then running the form_valid method.
    def form_valid(self, form):
        form.instance.author = self.request.user
        if "<p>" in form.instance.article_image:
            print("I found a p-tag")
            form.instance.article_image = form.instance.article_image[3:-4]
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'article_image', 'topics']

    def form_valid(self, form):
        form.instance.author = self.request.user
        if "<p>" in form.instance.article_image:
            print("I found a p-tag")
            form.instance.article_image = form.instance.article_image[3:-4]
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