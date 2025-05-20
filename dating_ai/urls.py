from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static
from chat.views import home 

# ✅ Define URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),  # Account APIs
    path('', home, name='home'),  # Homepage at /
    path('chat/', include('chat.urls')),
    path('api/matching/', include('matching.urls')),
  
]

# ✅ Serve static files in DEBUG mode
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
