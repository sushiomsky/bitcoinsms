"""
Checks bitcoind for any new payments.
This is a long running script that needs to be daemonized. Recommended to use
supervisord.org. In a development environment just running in a shell is
sufficient.
"""

from django.core.management.base import BaseCommand, CommandError
from bitcoinsms.api.models import Sms
from bitcoinsms.api.bitcoin import Bitcoin
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from time import sleep

class Command(BaseCommand):
    help = "Checks bitcoind for any new payments"

    def handle(self, *args, **options):

        bitcoin = Bitcoin()

        self.stdout.write("Starting")
        while(True):
            self.stdout.flush() # Required to see the data in supervisord logs
            records = Sms.objects.filter(status=Sms.WAITING_FOR_PAYMENT)

            if not records:
                sleep(1)
                continue

            for r in records:
                # With this debug setting it will skip Bitcoin and just mark a
                # payment as recieved after 1 minute from created time
                if settings.DEBUG_FAKE_BITCOIN:
                    time_threshold = timezone.now() - timedelta(minutes=1)
                    if r.time_created < time_threshold:
                        self.stdout.write("{address} DEBUG_FAKE_BITCOIN".format(
                            address=r.payment_address
                        ))
                        r.status = Sms.PREPARING_TO_SEND
                        r.status_message = "DEBUG_FAKE_BITCOIN"
                        r.time_payment_recieved = timezone.now()
                        r.save()
                    continue

                balance = int(bitcoin.rpc.getreceivedbyaddress(r.payment_address, 0)*100000000)
                if(balance >= r.cost_in_satoshis):
                    self.stdout.write("{address} was paid".format(
                        address=r.payment_address
                    ))
                    r.status = Sms.PREPARING_TO_SEND
                    r.status_message = "System will deliver your SMS message shortly"
                    r.time_payment_recieved = timezone.now()
                    r.save()

            sleep(1)
