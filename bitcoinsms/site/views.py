from django.conf import settings
from django.http import HttpResponse
from django.template import RequestContext, loader

def home(request):
    """
    Ahh the home page
    """

    template = loader.get_template('index.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def docs(request):
    """
    The Api documentation
    """

    template = loader.get_template('docs.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def faq(request):
    """
    Frequently Asked Questions
    """

    template = loader.get_template('faq.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))
