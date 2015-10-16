"""
Singleton pattern for bitcoinrpc
"""

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from django.conf import settings

class Bitcoin(object):
    __instance = None
    def __new__(cls):
        if Bitcoin.__instance is None:
            Bitcoin.__instance = object.__new__(cls)
        return Bitcoin.__instance

    def __init__(self):
        self.rpc = AuthServiceProxy('http://{username}:{password}@{host}'.format(
            host = settings.BITCOIN_RPC_HOST,
            username = settings.BITCOIN_RPC_USERNAME,
            password = settings.BITCOIN_RPC_PASSWORD
        ))
