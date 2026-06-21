from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Authentication
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Profile
    path('profile/', views.profile_view, name='profile'),
    path('profile/complete/', views.complete_profile_view, name='complete_profile'),

    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/log-meal/', views.log_meal_view, name='log_meal'),

    # Image Upload
    path('upload/', views.image_upload_view, name='image_upload'),

    # Chatbot
    path('chatbot/', views.chatbot_view, name='chatbot'),
    path('chatbot/clear/', views.clear_chat_view, name='clear_chat'),

    # BMI Calculator
    path('bmi/', views.bmi, name='bmi'),
]
