from django.urls import path
from . import views
app_name = 'EA'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('search/', views.search, name='search'),
]


urlpatterns += [
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
]


urlpatterns += [
    path('api/books/', views.BookListAPIView.as_view(), name='api-book-list'),
    path('api/books/<int:pk>/', views.BookDetailAPIView.as_view(), name='api-book-detail'),
    path('api/authors/', views.AuthorListAPIView.as_view(), name='api-author-list'),
    path('api/authors/<int:pk>/', views.AuthorDetailAPIView.as_view(), name='api-author-detail'),
]