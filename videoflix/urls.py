from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from videos.views import VideoViewSet 
from django.conf.urls.static import static
from django.conf import settings
from debug_toolbar.toolbar import debug_toolbar_urls
import debug_toolbar

router = DefaultRouter()
router.register(r"videos", VideoViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),  
    path('django-rq/', include('django_rq.urls'))
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]


