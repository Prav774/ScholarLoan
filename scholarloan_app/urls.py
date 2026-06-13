from django.urls import path, re_path
from django.shortcuts import redirect
from . import views
from .views import find_scholarships


from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('find-scholarships/', views.find_scholarships, name='find_scholarships'),
    
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("find-scholarships/", find_scholarships, name="find_scholarships"),
     path("chatbot/", lambda request: render(request, "chatbot.html"), name="chatbot"),     
     
]
