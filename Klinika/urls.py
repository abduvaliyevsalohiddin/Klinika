from django.contrib import admin
from django.urls import path, include

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Amaliyot uchun yozilgan KLINIKA API",
        default_version="V1",
        description="Test",
        contact=openapi.Contact("Abduvaliyev Salohiddin. Email: abduvaliyevsalohiddin568@gmail.com")
    ),
    public=True,
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('docs2/', schema_view.with_ui('redoc', cache_timeout=0)),

    path('register/', include("register.urls")),
    path('xonalar/', include("xonalar.urls")),
    path('tolovlar/', include("tolovlar.urls"))
]
