#!/usr/bin/python3
# -*- encoding: UTF-8 -*-

from datetime import datetime
from http.server import HTTPServer

import lib.roark.hypervisor as roark_hypervisor
from medium.RestAPI import RestAPIHandler
import bot.dummy
import medium.dummy


#TODO:
# > rotating log of recent queries with timestamp, remote ip, queried url

roark_status = {'started_date_utc': datetime.utcnow(),
                'started_date_local': datetime.now()}

if __name__ == '__main__':
    medium.dummy.dummy.roark_status = roark_status;
    
    #roark_hypervisor.add_api_key(medium.dummy.dummy, 'dummykey')
    #roark_hypervisor.add_api_key(RestAPIHandler, 'RestAPIkey')
    roark_hypervisor.add_bot(RestAPIHandler, bot.dummy.dummy(), 'dummy')
    
    server = HTTPServer(('localhost', 8080), RestAPIHandler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()
