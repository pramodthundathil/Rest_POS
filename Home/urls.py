from django.urls import path 
from .import views  
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("SignUp",views.SignUp,name="SignUp"),
    path("Index",views.Index,name="Index"),
    path('',views.SignIn,name="SignIn"),
    path('SignOut', views.SignOut, name='SignOut'),
    path("ListUser",views.ListUser,name="ListUser"),
    path("AddUser",views.AddUser,name="AddUser"),
    path("DeleteUser/<int:pk>",views.DeleteUser,name="DeleteUser")
]