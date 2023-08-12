from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('', include('user_app.urls')),
    path('', include('övning_app.urls')),
    path('api/', include('api.urls')),

]
