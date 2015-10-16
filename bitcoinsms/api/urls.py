from django.conf.urls import url
from bitcoinsms.api import views

urlpatterns = [
    url(r'^sms$', views.new_sms),
    url(r'^sms/(?P<payment_address>[a-zA-Z0-9]+)$', views.view_sms)
]
