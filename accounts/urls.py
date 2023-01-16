from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('user/', views.UserList.as_view(), name = 'user_list'),
    path('user/<int:pk>', views.UserDetail.as_view(), name='user_detail'),
    path('user/signup', views.SignUpView.as_view(), name = 'user_singup'),
    path('user/login', views.LoginView.as_view(), name = 'user_login'),
]