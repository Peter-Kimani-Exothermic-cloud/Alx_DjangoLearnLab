from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    PostListView, PostDetailView,
    PostCreateView, PostUpdateView,
    PostDeleteView, CommentDeleteView, CommentUpdateView,
    PostDetailView
)

from .views import search_posts
from .views import TagPostListView

urlpatterns = [
    path('register/', views.register, name='register' ),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('search/', search_posts, name='search_results'),
    path('tag/<slug:tag_slug>/', TagPostListView.as_view(), name='post_by_tag'),
    
    #CRUD Views Urls
    path('', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),

    #Comment Urls
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    
    # New URLs for comment CRUD
    # We use the comment's primary key (pk) to identify which comment to edit/delete
    path('comment/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment_edit'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),

]