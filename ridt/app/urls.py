from django.urls import path
from .views import PostListView, PostDetailView,  PostCreateView, PostUpdateView,  PostDeleteView
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', views.home, name='app-home'),
    path('blog/', PostListView.as_view(), name='app-blog'),
    path('blog/post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('blog/post/new/', PostCreateView.as_view(), name='post-create'),
    path('blog/post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('blog/post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('user/login/', views.user_login, name='user_login'),
    path('user/logout/', views.user_logout, name='user_logout'),
    path('user/register/', views.user_register, name='user_register'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
