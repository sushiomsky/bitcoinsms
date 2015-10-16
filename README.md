# bitcoinsms

RESTful API server for clients to send SMS text messages for bitcoin. Python [Django REST Framework](http://www.django-rest-framework.org/) is the framework used.

Demo is running at: [BitcoinSMS.io](https://bitcoinsms.io)

[This was built as a proof of concept](https://justinguy.github.io/2015/10/16/bitcoinsms/). I will do my best to provide some documentation, feel free to email me if you need additional help.

## Requirements
The application is currently using [Nexmo](https://www.nexmo.com/), but should be trivial to change. You will need a Nexmo account with a some US phone numbers added to it.

You can see the steps and configurations used to host BitcoinSMS.io in the [`deployment_resources`](https://github.com/justinguy/bitcoinsms/tree/master/deployment_resources) folder.

- Server requirements are:
  - `python3`
  - `python3-pip`
  - web server (recommended `apache2` & `libapache2-mod-wsgi-py3`)
  - some sort of daemonization (recommend `supervisord`)
- Python requirements are (can be installed with `pip3 install`):
  - `django`
  - `djangorestframework`
  - `django-ipware`
  - `nexmo`
  - `python-bitcoinrpc` (may not be able to use pip3 because package is old)
- Bitcoin
  - You need a full node with wallet support that accepts RPC.

## Settings

The main settings are in the standard Django location of `bitcoinsms/settings.py`. In addition you will need to create `bitcoinsms/settings_local.py`, see the bottom of `settings.py` for what settings are required.

To setup Django you will need to run:
    `python3 manage.py migrate`
    `python3 manage.py collectstatic`
 
Two daemons need to be setup. One watches for payments as they arrive in Bitcoin, the other sends text messages that have been paid. The best way to run these is with Supervisor (configuration example is in the `deployment_resources` folder).
- `python3 manage.py payments`
- `python3 manage.py send`

## Debug modes

It is possible to easily run the application for development without Nexmo or a Bitcoin node. To do so set `DEBUG_FAKE_BITCOIN` and `DEBUG_FAKE_SENDING` in your local settings file. Fake Bitcoin will tell the `payments` daemon to skip calling Bitcoin RPC and just mark an SMS as paid after one minute of creation. Fake sending just skips calling Nexmo and marks the SMS as successfully sent.
