from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('app_auth.urls')),
    # path('api/', include('app_user.urls')),
    path('api/', include('app_shop.urls')),
    path('api/', include('app_order.urls')),
    path('api/', include("api.urls")),
    path("", include("frontend.urls")),
]

if settings.DEBUG:
    urlpatterns.extend(
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )
