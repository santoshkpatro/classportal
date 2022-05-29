from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_view),
    path('profile/', views.ProfileView.as_view())
]