from rest_framework import generics
from .serializer import UserSerialier
from .models import User

# urlpatterns = [
#     path('accounts/login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
#     path('account/logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
#     path('account/signup/', views.sign_up, name='signup'),

# ]
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class =UserSerialier

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerialier