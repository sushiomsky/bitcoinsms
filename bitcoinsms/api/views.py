from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from bitcoinsms.api.models import Sms
from bitcoinsms.api.serializers import PrivateSmsSerializer, PublicSmsSerializer
from ipware.ip import get_real_ip
from django.conf import settings
from django.core.exceptions import ValidationError
import re

@api_view(['POST'])
def new_sms(request):
    """
    Create a new SMS message ready to send
    """

    # Get the IP address of the client
    ip_address = get_real_ip(request)
    if settings.DEBUG and ip_address is None:
        ip_address = "127.0.0.1"
    if ip_address is None:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    # Make the API a little more friendly by accepting numbers in strange formats
    # and trying to fix them up.
    if 'to' in request.data:
        new_to = re.sub('[^0-9]','', request.data['to'])
        if len(new_to) is 10:
            new_to = '1' + new_to
        new_to = '+' + new_to
        request.data['to'] = new_to

    serializer = PrivateSmsSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    sms = serializer.save(ip_address=ip_address)

    public_serializer = PublicSmsSerializer(sms)
    return Response(public_serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def view_sms(request, payment_address):
    """
    Get the status of an SMS
    """
    try:
        sms = Sms.objects.get(payment_address=payment_address)
    except Sms.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = PublicSmsSerializer(sms)

    return Response(serializer.data)
