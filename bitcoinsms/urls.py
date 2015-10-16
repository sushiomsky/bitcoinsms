from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^api/', include('bitcoinsms.api.urls')),
    url(r'^', include('bitcoinsms.site.urls'))
]
