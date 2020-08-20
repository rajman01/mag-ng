from django.urls import path
from django.contrib.auth import views as auth_views
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('', views.api_root),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('profile/<int:pk>/', views.Profile.as_view(), name='profile'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('article/', views.ArticleList.as_view(), name='articles'),
    path('article/<int:pk>/', views.ArticleDetail.as_view(), name='article-detail'),
    path('search/', views.SearchList.as_view(), name='search'),
]

urlpatterns = format_suffix_patterns(urlpatterns)