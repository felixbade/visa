import logging
from os import fork

from app import app

pid = 0#fork()
if pid > 0:
    print('PID: %d' % pid)
    exit(0)
elif pid < 0:
    print('Could not fork: %d' % pid)
    exit(1)

# we are behind a proxy. log the ip of the end-user, not the proxy.
# this will also work without a proxy
import werkzeug.serving
werkzeug.serving.WSGIRequestHandler.address_string = lambda self: self.headers.get('x-real-ip', self.client_address[0])

# log to a file (log.txt), not stderr
logging.basicConfig(filename='log.txt', level=logging.DEBUG, format='%(message)s')

app.run(port=3010, debug=True)
