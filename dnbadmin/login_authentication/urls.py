from django.urls import path
from .views import Logout, SignUp, Login

urlpatterns = [
    path('signin/', Login.as_view(), name='signin'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('logout/', Logout.as_view(), name='logout')
]
