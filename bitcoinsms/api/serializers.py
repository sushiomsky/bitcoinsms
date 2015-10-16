from rest_framework import serializers
from bitcoinsms.api.models import Sms

class PrivateSmsSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    cost_in_btc = serializers.SerializerMethodField()
    payment_uri = serializers.SerializerMethodField()

    class Meta:
        model = Sms
        fields = (
            'status',
            'status_message',
            'payment_address',
            'time_created',
            'time_payment_recieved',
            'time_sent',
            'cost_in_satoshis',
            'cost_in_btc',
            'payment_uri',
            'ip_address',
            'to',
            'text'
        )

    def get_status(self,obj):
        return obj.get_status_display()

    def get_cost_in_btc(self,obj):
        return obj.cost_in_satoshis / 100000000

    def get_payment_uri(self,obj):
        amount = obj.cost_in_satoshis / 100000000
        address = obj.payment_address
        return "bitcoin:{address}?amount={amount}".format(
            address=address,
            amount=amount
        )


class PublicSmsSerializer(PrivateSmsSerializer):
    class Meta:
        model = Sms
        fields = (
            'status',
            'status_message',
            'payment_address',
            'time_created',
            'time_payment_recieved',
            'time_sent',
            'cost_in_satoshis',
            'cost_in_btc',
            'payment_uri',
        )
