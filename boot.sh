adduser --disabled-password --gecos '' r
cd /g2e/
mod_wsgi-express setup-server wsgi.py --port=80 --user r --group r --server-root=/etc/g2e --socket-timeout=600 --limit-request-body=524288000
chmod a+x /etc/g2e/handler.wsgi
chown -R r /g2e/g2e/static/
/etc/g2e/apachectl start
tail -f /etc/g2e/error_log