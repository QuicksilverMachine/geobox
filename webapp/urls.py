from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static

from webapp.views import index

urlpatterns = [
    url(r'^$', index),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^map/', include('map.urls', namespace="map")),
]

handler404 = 'orpheus.views.page_not_found_view'
handler500 = 'orpheus.views.error_view'
handler403 = 'orpheus.views.permission_denied_view'
handler400 = 'orpheus.views.bad_request_view'

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
