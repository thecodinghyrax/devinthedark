from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, TopicPostListView, SearchPostListView

# Info:
# The url patterns are directed to a certain view which handels the logic
# and then renders a template. 

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    # path('', views.home, name='blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('search/', SearchPostListView.as_view(), name='search-posts'),
    path('topic/<str:topic>/', TopicPostListView.as_view(), name='topic-posts'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'), # Template is the same as below by default
    path('post/new/', PostCreateView.as_view(), name='post-create'), # Template is <model>_form This is specific to the CreateView class
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'), 
]

#function   url path                   Django View     name used by the url funtion in templates       
#   |           |                           |                         |
# path('search/<str:topic>/', SearchPostListView.as_view(), name='search-posts'),
# class based views look for html templates with this naming convention:
# <app>/<model>_<viewtype>.html