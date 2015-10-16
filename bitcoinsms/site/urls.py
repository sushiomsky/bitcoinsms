from django.conf.urls import url
from bitcoinsms.site import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^docs$', views.docs),
    url(r'^faq$', views.faq)
]
