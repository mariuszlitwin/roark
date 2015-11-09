#!/usr/bin/python3
# -*- encoding: UTF-8 -*-

from datetime import datetime
from http.server import HTTPServer

from medium.RestAPI import RestAPIHandler
import bot.dummy
import medium.dummy

#TODO:
# > rotating log of recent queries with timestamp, remote ip, queried url
# > some fancy method for adding per-medium bots (this class tweak below looks fine, get registered bot outside status, provide some wrapper for adding new bots)

roark_status = {'started_date_utc': datetime.utcnow(),
                'started_date_local': datetime.now(),
                'registered_bot': dict()}

if __name__ == '__main__':
    roark_status['registered_bot']['dummy'] = bot.dummy.dummy()
    medium.dummy.dummy.roark_status = roark_status;
    server = HTTPServer(('localhost', 8080), RestAPIHandler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()
