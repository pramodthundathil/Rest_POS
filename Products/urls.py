from django.urls import path 
from .import views  


urlpatterns = [
    path("PosIndex",views.PosIndex,name="PosIndex"),
    path("List_Category",views.List_Category,name="List_Category"),
    path("Add_Category",views.Add_Category,name="Add_Category"),
    path("DeleteCategory/<int:pk>",views.DeleteCategory,name="DeleteCategory"),
    path("Add_Product",views.Add_Product,name="Add_Product"),
    path("List_Product",views.List_Product,name="List_Product"),
    path("DeleteProduct/<int:pk>",views.DeleteProduct,name="DeleteProduct"),
    path("EditProduct/<int:pk>",views.EditProduct, name = "EditProduct"),
    path("list_add_ons",views.list_add_ons, name = "list_add_ons"),
    path("add_add_ons",views.add_add_ons, name = "add_add_ons"),

    path("Pos",views.Pos,name="Pos"),
    path("Add_Table",views.Add_Table,name="Add_Table"),
    path("List_Table",views.List_Table,name="List_Table"),
    path("Delete_Table/<int:pk>",views.Delete_Table,name="Delete_Table"),


    path("CreateOrder",views.CreateOrder,name="CreateOrder"),
    path("OrderSingle/<int:pk>",views.OrderSingle,name="OrderSingle"),
    path("add_to_order",views.add_to_order,name="add_to_order"),
    path('increase_quantity', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity', views.decrease_quantity, name='decrease_quantity'),
    path("Delete_menuitem/<int:pk>",views.Delete_menuitem,name="Delete_menuitem"),
    path("TakeOrder/<int:pk>",views.TakeOrder,name="TakeOrder"),
    path('receipt/<int:order_id>/', views.receipt_view, name='receipt'),
    path("add_items_to_order/<int:pk>/<int:id>",views.add_items_to_order,name="add_items_to_order"),
    path("add_on_to_item/<int:pk>/<int:id>",views.add_on_to_item,name="add_on_to_item"),


    path('KitchenDashboard', views.KitchenDashboard, name='KitchenDashboard'),
    path('refresh_table', views.refresh_table, name='refresh_table'),
    path('refresh_order', views.refresh_order, name='refresh_order'),
    path('Status_Change', views.Status_Change, name='Status_Change'),
    path('Status_Change_Order_Ready', views.Status_Change_Order_Ready, name='Status_Change_Order_Ready'),
    path('Status_Change_OrderCompeletion/<int:pk>', views.Status_Change_OrderCompeletion, name='Status_Change_OrderCompeletion'),
    path('Status_Change_Menu_Finish', views.Status_Change_Menu_Finish, name='Status_Change_Menu_Finish'),
    path('SettleOrder/<int:pk>', views.SettleOrder, name='SettleOrder'),
    path('ViewCheckouts', views.ViewCheckouts, name='ViewCheckouts'),
    path('search-menu/', views.search_menu, name='search_menu'),


    path('Reports', views.Reports, name='Reports'),
    path('generate_excel_report', views.generate_excel_report, name='generate_excel_report'),
    path('generate_orders_report', views.generate_orders_report, name='generate_orders_report'),


    path('AddTax', views.AddTax, name='AddTax'),
    path('ListTax', views.ListTax, name='ListTax'),






    
]    