from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'users'

urlpatterns = [
    path('registration/', views.RegisterView.as_view(), name='registration'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/<str:username>/edit/', views.ProfileUpdateView.as_view(), name='edit_profile'),
]
