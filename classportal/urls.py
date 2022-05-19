from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('api/auth/', include('api.auth.urls')),
    path('api/exams/', include('api.exams.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('exams/', include('exams.urls')),
    path('', include('home.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
