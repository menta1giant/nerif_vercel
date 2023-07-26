from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/matches/', include('matches.urls')),
    path('api/v1/storage/', include('storage.urls')),
    path('api/v1/users/', include('users.urls')),
    path('api/v1/content/', include('content.urls')),
    path('api/v1/dashboards/', include('dashboards.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)