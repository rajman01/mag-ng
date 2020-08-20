from django . urls import path
from . import views

app_name = 'articles'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('create/', views.ArticleCreateView.as_view(), name='create'),
    path('write/<int:form_id>/', views.write_view, name='write'),
    path('edit/<int:pk>/', views.ArticleUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', views.ArticleDeleteView.as_view(), name='delete'),
    path('publish/<int:form_id>/', views.publish, name='publish'),
    path('detail/<int:pk>/', views.ArticleDetailView.as_view(), name='detail'),
    path('preview/<int:pk>/', views.PreviewView.as_view(), name='preview'),
    path('draft/', views.DraftView.as_view(), name='draft'),
    path('category/<category>/', views.CategoryView.as_view(), name='category'),
    path('recent/', views.RecentView.as_view(), name='recent'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('covid/', views.covid, name='covid')
]
