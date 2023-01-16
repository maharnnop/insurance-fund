from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('insure/', views.InsuranceList.as_view(), name = 'insure_list'),
    path('insure/create', views.InsuranceCreate.as_view(), name = 'insure_create'),
    path('insure/<int:pk>', views.InsuranceDetail.as_view(), name='insure_detail'),
    path('insure/invest/', views.InvestInsureList.as_view() , name = 'invest_insure_list'),
    path('insure/invest/<int:pk>', views.InvestInsureDetail.as_view(), name='invest_insure_detail'),
    path('insure/user/', views.UserInsureList.as_view() , name = 'user_insure_list'),
    path('insure/user/<int:pk>', views.UserInsureDetail.as_view(), name='user_insure_detail'),
]
