from django.urls import path
from .views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView

urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('post/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('post/create/', BlogCreateView.as_view(), name='blog_create'),
    path('post/<int:pk>/edit/', BlogUpdateView.as_view(), name='blog_edit'),
    path('post/<int:pk>/delete/', BlogDeleteView.as_view(), name='blog_delete'),
]
