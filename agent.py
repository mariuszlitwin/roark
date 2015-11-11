#!/usr/bin/python3
# -*- encoding: UTF-8 -*-

from datetime import datetime
from http.server import HTTPServer

import oth.roark.hypervisor as roark_hypervisor

from medium.dummy import dummy
from medium.RestAPI import RestAPIHandler

import bot.dummy
import bot.process
import bot.http
import bot.fs

#TODO:
# > rotating log of recent queries with timestamp, remote ip, queried url

roark_status = {'started_date_utc': datetime.utcnow(),
                'started_date_local': datetime.now()}

if __name__ == '__main__':
    dummy.roark_status = roark_status;
    
    #roark_hypervisor.add_api_key(medium.dummy.dummy, 'dummykey')
    #roark_hypervisor.add_api_key(RestAPIHandler, 'RestAPIkey')
    roark_hypervisor.add_bot(RestAPIHandler, bot.dummy.dummy(), 'dummy')
    roark_hypervisor.add_bot(RestAPIHandler, bot.process.process(), 'process')
    roark_hypervisor.add_bot(RestAPIHandler, bot.http.http(), 'http')
    roark_hypervisor.add_bot(RestAPIHandler, bot.fs.fs(), 'fs')
    
    server = HTTPServer(('localhost', 8080), RestAPIHandler)
    print('Starting server on localhost:8080, use <Ctrl-C> to stop')
    server.serve_forever()
