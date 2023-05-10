from django.urls import path
from . import views
urlpatterns = [
    path('', views.PostListView.as_view(), name= 'Blog-home'),
    path('home/', views.PostListView.as_view(), name= 'Blog-home'),
    path('about/', views.about, name= 'Blog-about'),  
    path('post/<int:pk>/', views.PostDetailView.as_view(), name= 'post-detail'),
    path('post/new/', views.PostCreateView.as_view(), name= 'post-create'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name= 'post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name= 'post-delete'),
    path('like/<int:pk>/', views.PostLikeView, name= 'post-like'),
    path('comment/<int:pk>/', views.PostCommentView.as_view(), name= 'post-comment'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),
]
