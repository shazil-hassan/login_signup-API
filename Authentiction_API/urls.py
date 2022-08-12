
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
   path(r'^api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('api/', include('acount.urls')),
    
]
