"""main url of tms project"""

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns


API_VERSION = 0.1

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'api/v{API_VERSION}/', include('core.urls')),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)

urlpatterns = format_suffix_patterns(urlpatterns)
