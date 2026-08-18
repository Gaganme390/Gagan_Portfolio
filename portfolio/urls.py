from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.site_title = settings.ADMIN_SITE_TITLE
admin.site.index_title = settings.ADMIN_INDEX_TITLE

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/chat/', include('chatbot.urls')),
    path('', include('core.urls')),
]

from django.views.static import serve
from django.urls import re_path

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
