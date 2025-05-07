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
    path("DeleteUser/<int:pk>",views.DeleteUser,name="DeleteUser"),
    path("PermissionDenyed",views.PermissionDenyed,name="PermissionDenyed"),


    path('get-overview-chart-data/', views.get_overview_chart_data, name='get_overview_chart_data'),
    path('get_top_products/', views.get_top_products, name='get_top_products'),
    path('get_order_summary/', views.get_order_summary, name='get_order_summary'),
    path('api/income/', views.get_income_data, name='get_income_data'),
    path('api/expense/', views.get_expense_data, name='get_expense_data'),
    path('api/popular-menu-items/', views.popular_menu_items, name='popular_menu_items'),
    
    

]
