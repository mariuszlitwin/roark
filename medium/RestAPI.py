#!/usr/bin/python3
# -*- encoding: UTF-8 -*-

import urllib.parse
import json
from http.server import BaseHTTPRequestHandler

from medium import dummy

from medium.exceptions import BotException, CommandException

class RestAPIHandler(BaseHTTPRequestHandler, dummy.dummy):
    error_content_type = 'text/json;charset=utf-8'
    error_message_format = json.dumps({'code': '%(code)d',
                                       'explanation': '%(explain)s',
                                       'message': '%(message)s'}, sort_keys=True,
                                                                  indent=4)

    def _parse_params(self):
        params = dict()
        
        if '?' in self.path:
            (params['path'], params['query']) = self.path.split('?')[:2]
            params['path'] = params['path'].replace('/', '')
            params['query'] = urllib.parse.parse_qs(params['query'],
                                                  keep_blank_values=True)
            for key in params['query']:
                if len(params['query'][key]) == 1:
                    params['query'][key] = params['query'][key][0]
        else:
            (params['path'], params['query']) = (self.path, dict())
    
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
        
        return params
        
    def _get_results(self, path, query):
        if path == '':
            return {'bot_count': len(self.roark_status['registered_bot']),
                    'bot_list': list(self.roark_status['registered_bot'].keys()),
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
        except BotException as e:
            self.send_error(code=404,
                            message=e.message)
            self.log_error(e.message)
            return False
        except CommandException as e:
            self.send_error(code=400,
                            message=e.message,
                            explain=e.explanation)
            self.log_error(explain=e.explanation)
            return False
        else:
            return self.do_HEAD(params=params, response=response)
            
    def do_GET(self):
        return self.do_POST()
        
    def do_PUT(self):
        return self.do_POST()
        
    def do_DELETE(self):
        return self.do_POST()
