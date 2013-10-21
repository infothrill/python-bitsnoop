# -*- coding: utf-8 -*-

import sys
from time import sleep
from multiprocessing import Process

from bottle import Bottle, run, response, route, request

if sys.version_info >= (3, 0):
    unicode = str

sample_data = {
               "03DBF6EBC059CD97ACAE7CAF308A0E050A7EC51A": "ERROR",
               "13DBF6EBC059CD97ACAE7CAF308A0E050A7EC51A": "NOTFOUND",
               "23DBF6EBC059CD97ACAE7CAF308A0E050A7EC51A": "VERIFIED",
               "33DBF6EBC059CD97ACAE7CAF308A0E050A7EC51A": "GOOD",
               "43DBF6EBC059CD97ACAE7CAF308A0E050A7EC51A": "NONE",
               "53DBF6EBC059CD97ACAE7CAF308A0E050A7EC51A": "BAD",
               "63DBF6EBC059CD97ACAE7CAF308A0E050A7EC51A": "FAKE",
               }


@route('/api/fakeskan.php')
def fakeskan():
    arg_json = request.query.json or '0'
    arg_hash = request.query.hash
    assert len(arg_hash) == 40
    assert arg_hash in sample_data
    assert arg_json in ('0', '1')
    response.content_type = 'application/json; charset=utf-8'
    if arg_json == '1':
        return unicode('"' + sample_data[arg_hash] + '"')
    else:
        return unicode(sample_data[arg_hash])


class BitsnoopFakeSkanApp(Bottle):
    def __init__(self, host='localhost', port=8000):
        super(BitsnoopFakeSkanApp, self).__init__()
        self.host = host
        self.port = port
        self.process = None
        self.route(path='/api/fakeskan.php', callback=fakeskan)

    def run(self):
        run(self, host=self.host, port=self.port, debug=True, quiet=False)

    def start(self):
        self.process = Process(target=self.run)
        self.process.start()
        sleep(1)

    def stop(self):
        self.process.terminate()
        self.process = None

    @property
    def url(self):
        return 'http://{}:{}'.format(self.host, self.port)


if __name__ == '__main__':
    BitsnoopFakeSkanApp('localhost', 8000).run()
