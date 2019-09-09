from django.urls import path
from . import views
from .views import (PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,
UserPostListView, CommentCreateView, FollowsListView, UserFollowView)

urlpatterns = [
        path('', PostListView.as_view(), name='blog-home'),
        path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
        path('user/<str:username>/follow/', UserFollowView.as_view(), name='follow'),
        path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
        path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
        path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
        path('post/new/', PostCreateView.as_view(), name='post-create'),
        path('post/<int:pk>/comment/', CommentCreateView.as_view(), name='comment-create'),
        path('about/', views.about, name='blog-about'),
        path('follows/', FollowsListView.as_view(), name='follows'),

    ]
