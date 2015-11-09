#!/usr/bin/python3
# -*- encoding: UTF-8 -*-

import requests

import bot.dummy
import lib.roark.exceptions

class http(bot.dummy.dummy):
    def __init__(self):
        self.session = requests.Session()

    def request(self, path, query):
        response = None
        try:
            if len(path) == 1 and query['command'] == 'POST' and \
               'url' in query and 'method' in query:
                agent_request = requests.Request(query['method'], query['url'],
                                                 data = query.get('data', None),
                                                 headers = query.get('headers', None))
                p_agent_request = self.session.prepare_request(agent_request)
                resp = self.session.send(p_agent_request)
                response = {'status_code': resp.status_code}
                if 'no_content' not in query:
                    response['content'] = resp.text
            elif len(path) == 1 and query['command'] == 'GET':
                response = {'cookies': self.session.cookies.get_dict()}
            else:
                raise lib.roark.exceptions.CommandException("Invalid command.", None)
        except requests.exceptions.RequestException as e:
            raise lib.roark.exceptions.CommandException("Sending HTTP request failed.", str(e))
        return response
        
