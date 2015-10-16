"""
Send SMSs as they become ready.
This is a long running script that needs to be daemonized. Recommended to use
supervisord.org. In a development environment just running in a shell is
sufficient.
"""

from django.core.management.base import BaseCommand, CommandError
from bitcoinsms.api.models import Sms
from django.utils import timezone
from django.conf import settings
from time import sleep
import nexmo, sys

class Command(BaseCommand):
    help = "Send SMSs that are ready"

    def handle(self, *args, **options):
        client = nexmo.Client(
            key=settings.NEXMO_API_KEY,
            secret=settings.NEXMO_API_SECRET
        )

        self.stdout.write("Starting")
        while(True):
            self.stdout.flush() # Required to see the data in supervisord logs
            records = Sms.objects.filter(status=Sms.PREPARING_TO_SEND)

            if not records:
                sleep(1)
                continue

            # With this debug setting messages will just be marked as sent
            # without sending to them to the provider for delivery
            if settings.DEBUG_FAKE_SENDING:
                for r in records:
                    r.status = Sms.SENT_SUCCESSFULLY
                    r.status_message = "DEBUG_FAKE_SENDING"
                    r.save()
                    self.stdout.write("{address} DEBUG_FAKE_SENDING".format(
                        address=r.payment_address
                    ))
                continue

            for r in records:
                status = 99
                status_message = "Unknown Critical Error"

                data = {
                    'from': settings.SMS_NUMBER_FROM,
                    'to': r.to,
                    'text': r.text
                }

                self.stdout.write("Sending {address}: {data}".format(
                    address=r.payment_address,
                    data=data
                ))
                try:
                    response = client.send_message(data)
                    response = response['messages'][0]
                    status = response['status']

                    if status is not '0':
                        status_message = "{code}:{text}".format(
                            code=status,
                            text=response['error-text']
                        )
                    else:
                        status_message = response['message-id']
                except nexmo.AuthenticationError:
                    status_message = "Authentication Error"
                except nexmo.Error:
                    status_message = "Nexmo API connection error"
                except:
                    pass

                self.stdout.write(" Response: {code}:{message}".format(
                    code=status,
                    message=status_message
                ))

                if status is '0':
                    r.status = Sms.SENT_SUCCESSFULLY
                else:
                    r.status = Sms.ERROR_ON_SEND

                r.time_sent = timezone.now()
                r.status_message = status_message
                r.save()

                sleep(1) # Needed to keep from getting slapped by Nexmo

            sleep(1)
