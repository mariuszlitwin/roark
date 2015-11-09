#!/usr/bin/python3
# -*- encoding: UTF-8 -*-

from datetime import datetime
from http.server import HTTPServer

from medium.RestAPI import RestAPIHandler
from bot.dummy import dummy

roark_status = {'started_date_utc': datetime.utcnow(),
                'started_date_local': datetime.now(),
                'registered_bot': dict()}

if __name__ == '__main__':
    roark_status['registered_bot']['dummy'] = dummy()
    server = HTTPServer(('localhost', 8080), RestAPIHandler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()
