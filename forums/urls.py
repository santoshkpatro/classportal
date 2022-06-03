from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.post_list, name='forums_post_list'),
    path('posts/create/', views.post_create, name='forums_post_create'),
    path('posts/<uuid:post_id>/comments/add/', views.post_comment_add, name='forums_post_comment_add')
]