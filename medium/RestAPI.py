#!/usr/bin/python3
# -*- encoding: UTF-8 -*-

import urllib.parse
import json
from http.server import BaseHTTPRequestHandler

import medium

from oth.roark.exceptions import BotException, CommandException, AccessException

class RestAPIHandler(BaseHTTPRequestHandler, medium.dummy.dummy):
    error_content_type = 'text/json;charset=utf-8'
    error_message_format = json.dumps({'code': '%(code)d',
                                       'explanation': '%(explain)s',
                                       'message': '%(message)s'}, sort_keys=True,
                                                                  indent=4)

    def _parse_params(self):
        params = dict()
        
        if '?' in self.path:
            (params['path'], params['query']) = self.path.split('?')[:2]
            params['query'] = urllib.parse.parse_qs(params['query'],
                                                  keep_blank_values=True)
            for key in params['query']:
                if len(params['query'][key]) == 1:
                    params['query'][key] = params['query'][key][0]
        else:
            (params['path'], params['query']) = (self.path, dict())
        params['path'] = params['path'].strip('/').split('/')
    
        payload = None
        payload_length = int(self.headers.get('Content-Length', failobj='0'))
        if payload_length:
            payload = self.rfile.read(payload_length).decode('UTF-8')
            try:
                payload = json.loads(payload)
                params['query'].update(payload)
            except ValueError as e:
                raise CommandException('Payload is not valid JSON document', str(e))
                
        params['query']['command'] = self.command
        
        self.check_access(params['query'].get('access_token', ''))
        
        return params
        
    def _get_results(self, path, query):
        if path[0] == '':
            return {'bot_count': len(self.bot_list),
                    'bot_list': list(self.bot_list.keys()),
                    'started_date_utc': self.roark_status['started_date_utc'].strftime('%Y-%m-%dT%H:%M:%S.%f')}
        else:
            return self.query_bot(path=path,
                                  query=query)
    
    def do_HEAD(self, 
                params=None,
                response=None,
                status_code=200):
        self.send_response(status_code)
        self.send_header("Content-type", "text/json")
        self.end_headers()
        
        if response:
            if 'pretty' in params['query']:
                self.wfile.write(bytes(json.dumps(response,
                                                  indent=4, 
                                                  sort_keys=True), 'UTF-8'))
            else:
                self.wfile.write(bytes(json.dumps(response), 'UTF-8'))
        
        return True
 
    def do_POST(self):
        try:
            params = self._parse_params()
            response = self._get_results(params['path'], params['query'])
        except AccessException as e:
            self.send_error(code=401,
                            message=e.message)
            return False
        except BotException as e:
            self.send_error(code=404,
                            message=e.message)
            return False
        except CommandException as e:
            self.send_error(code=400,
                            message=e.message,
                            explain=e.explanation)
            return False
        else:
            return self.do_HEAD(params=params, response=response)
            
    def do_GET(self):
        return self.do_POST()
        
    def do_PUT(self):
        return self.do_POST()
        
    def do_DELETE(self):
        return self.do_POST()
