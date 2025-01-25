from django.contrib import admin
from django.urls import path, include 
from django.conf import settings
from django.conf.urls.static import static
from Home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include("Home.urls")),
    path("Products/",include('Products.urls')),
  
   
    
]
urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)


handler404 = views.custom_page_not_found_view
handler500 = views.custom_server_error_view
handler403 = views.custom_permission_denied_view
handler400 = views.custom_bad_request_view