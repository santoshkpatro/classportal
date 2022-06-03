from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.post_list, name='forum_post_list')
]