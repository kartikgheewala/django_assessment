from django.urls import path
from users import views

urlpatterns = [
    path('user/create', views.UserCreateView.as_view(), name='user_register'),
    path('login', views.LoginView.as_view(), name='login'),
]
