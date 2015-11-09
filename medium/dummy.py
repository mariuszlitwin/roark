#!/usr/bin/python3
# -*- encoding: UTF-8 -*-

import time
import hashlib

import lib.roark.exceptions 

class dummy:
    roark_status = dict()
    bot_list = dict()
    api_key = None;

    def check_access(self, received_access_token):
        if self.api_key:
            m = hashlib.md5()
            m.update(self.api_key.encode('utf-8'))
            m.update(bytes(int(time.time())))

            if m.hexdigest() != received_access_token:
                raise lib.roark.exceptions.AccessException('Access Token mismatch! Check your local time settings and used api-key.')

    def query_bot(self, path, query):
        if path[0] in self.bot_list:
            return self.bot_list[path[0]].request(path, query)
        else:
            raise lib.roark.exceptions.BotNotFoundException('No bot registered under {path}'.format(path=path))
            return None
