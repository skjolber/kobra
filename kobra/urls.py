# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin

from .views import health_view, web_client_view


urlpatterns = [
    url(r'^health/$', health_view),
    url(r'^api/v1/', include('kobra.api.v1.urls', namespace='v1')),

    url(r'^admin/', include(admin.site.urls)),

    # Matches everything* and therefore must come last.
    # *everything except /static/... since this breaks the static file serving.
    url(r'^(?!static/)', include([
        url(r'^$', web_client_view, name='home'),
        url(r'^.*/$', web_client_view)
    ], namespace='web-client'))
]
