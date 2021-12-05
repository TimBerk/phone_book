from rest_framework import routers

from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path

from phone_book.yasg import schema_view

from book.api.routers import router as book_router


router = routers.DefaultRouter()
router.registry.extend(book_router.registry)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/token/', include('djoser.urls.jwt')),
    url(r'api/v1/$', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema-ui'),
    url(r'api/v1/redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/v1/', include(router.urls)),
]
