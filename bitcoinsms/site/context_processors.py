from django.conf import settings

def site_name(request):
    return {'SITE_NAME': settings.SITE_NAME}

def base_url(request):
    return {'BASE_URL': settings.BASE_URL}
