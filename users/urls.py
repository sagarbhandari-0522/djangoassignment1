from django.urls import path
from .views import UserRegisterAPIView, UserLoginAPIView, UserLogoutAPIView,UserList

urlpatterns = [
    path("register/", UserRegisterAPIView().as_view(), name="user_register"),
    path("login/", UserLoginAPIView().as_view(), name="user_login"),
    path('users-list/', UserList.as_view(), name='user-list'),
    path("logout/", UserLogoutAPIView().as_view(), name="user_logout")
]

