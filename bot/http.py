#!/usr/bin/python3
# -*- encoding: UTF-8 -*-

import requests
import os.path
import tempfile

import bot.dummy
import oth.roark.exceptions

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
                resp = self.session.send(p_agent_request, stream=True)
                response = {'status_code': resp.status_code}
                if 'no_content' not in query:
                    response['content'] = resp.text
                if 'download' in query:
                    filename = query['url'][query['url'].rfind('/') + 1:]
                    if not filename:
                        filename = 'default'
                    download_path = os.path.join(tempfile.gettempdir(),
                                                 filename)
                    with open(download_path, 'wb') as fh:
                        for chunk in resp.iter_content(1024):
                            fh.write(chunk)
                    response['download_path'] = download_path;
            elif len(path) == 1 and query['command'] == 'GET':
                response = {'cookies': self.session.cookies.get_dict()}
            else:
                raise oth.roark.exceptions.CommandException("Invalid command.", None)
        except requests.exceptions.RequestException as e:
            raise oth.roark.exceptions.CommandException("Sending HTTP request failed.", str(e))
        return response
