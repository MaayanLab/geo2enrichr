adduser --disabled-password --gecos '' r
cd /g2e/
mod_wsgi-express setup-server wsgi.py --port=80 --user r --group r --server-root=/etc/g2e
chmod a+x /etc/g2e/handler.wsgi
/etc/g2e/apachectl start
tail -f /etc/g2e/error_log
