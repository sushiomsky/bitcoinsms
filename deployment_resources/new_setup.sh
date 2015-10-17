apt-get install apache2
apt-get install python3
apt-get install python3-pip
apt-get install libapache2-mod-wsgi-py3
apt-get install supervisor

pip3 install django
pip3 install djangorestframework
pip3 install django-ipware
pip3 install nexmo

## This is a little bit of a hack because Python 3 bugs have not been merged
## into python-bitcoinrpc yet.
cd /tmp
git clone CHECKFORFIXhttps://github.com/alecalve/python-bitcoinrpc.git
cd python-bitcoinrpc
python3 setup.py install

cd /opt
git clone https://github.com/justinguy/bitcoinsms.git
rm /opt/bitcoinsms/deployment_resources/00*
cp /opt/bitcoinsms/deployment_resources/001-bitcoinsms.conf /etc/apache2/sites-enabled/
## PUT SSL CERTS IN /opt/ssl/

nano /opt/bitcoinsms/bitcoinsms/settings_local.py
    # Put secret stuff in here

a2enmod ssl
a2enmod rewrite
a2enmod headers

cd /opt/bitcoinsms
python3 manage migrate
python3 manage.py collectstatic

apachectl restart

service supervisor stop
update-rc.d supervisor disable
update-rc.d -f supervisor remove
supervisord -c /opt/bitcoinsms/deployment_resources/supervisord.conf

iptables-restore < /opt/bitcoinsms/deployment_resources/iptables.up.rules
ip6tables-restore < /opt/bitcoinsms/deployment_resources/ip6tables.up.rules

nano /etc/network/interfaces
  # ADD TO eth0:
  #   post-up iptables-restore < /opt/bitcoinsms/deployment_resources/iptables.up.rules
  #   post-up ip6tables-restore < /opt/bitcoinsms/deployment_resources/ip6tables.up.rules
