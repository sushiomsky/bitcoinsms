from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from bitcoinsms.api.bitcoin import Bitcoin
from django.conf import settings
from binascii import hexlify
from os import urandom

class Sms(models.Model):
    class Meta:
        db_table = "sms"

    WAITING_FOR_PAYMENT = 0
    PREPARING_TO_SEND = 1
    SENT_SUCCESSFULLY =2
    ERROR_ON_SEND = 3
    STATUS_CHOICES = (
        (WAITING_FOR_PAYMENT, 'WAITING_FOR_PAYMENT'),
        (PREPARING_TO_SEND, 'PREPARING_TO_SEND'),
        (SENT_SUCCESSFULLY, 'SENT_SUCCESSFULLY'),
        (ERROR_ON_SEND, 'ERROR_ON_SEND')
    )

    status = models.PositiveSmallIntegerField(default=WAITING_FOR_PAYMENT, choices=STATUS_CHOICES, editable=False, db_index=True)
    payment_address = models.CharField(max_length=35, editable=False, unique=True, db_index=True)
    time_created = models.DateTimeField(auto_now_add=True, editable=False)
    time_payment_recieved = models.DateTimeField(blank=True, null=True, editable=False)
    time_sent = models.DateTimeField(blank=True, null=True, editable=False)
    cost_in_satoshis = models.PositiveIntegerField(editable=False)
    ip_address = models.GenericIPAddressField(editable=False)
    to_regex = RegexValidator(regex=r'^\+?1?\d{11}$', message="Number invalid, suggested format: '333-555-6666'")
    to = models.CharField(max_length=12,validators=[to_regex])
    text = models.CharField(max_length=160)
    status_message = models.CharField(max_length=255, editable=False)

    def save(self, **kwargs):
        if not self.id:
            if settings.DEBUG_FAKE_BITCOIN:
                self.payment_address = hexlify(urandom(16)).decode('utf8')
            else:
                bitcoin = Bitcoin()
                self.payment_address = bitcoin.rpc.getnewaddress()

            self.cost_in_satoshis = settings.SMS_COST_IN_SATOSHIS
            self.status_message = "Pay {amount} BTC to {address} to deliver the SMS".format(
                amount = self.cost_in_satoshis / 100000000,
                address = self.payment_address
            )
        super(Sms, self).save(**kwargs)
