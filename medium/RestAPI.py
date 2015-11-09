#!/usr/bin/python3
# -*- encoding: UTF-8 -*-

import urllib.parse
import json
from http.server import BaseHTTPRequestHandler

from bot import dummy

class RestAPIHandler(BaseHTTPRequestHandler):
    error_content_type = 'text/json;charset=utf-8'
    error_message_format = json.dumps({'code': '%(code)d',
                                       'explanation': '%(explain)s',
                                       'message': '%(message)s'}, sort_keys=True,
                                                                  indent=4)

    def _parse_args(self):
        args = dict()
        
        if '?' in self.path:
            (args['path'], args['query']) = self.path.split('?')[:2]
            args['query'] = urllib.parse.parse_qs(args['query'],
                                                  keep_blank_values=True)
            for key in args['query']:
                if len(args['query'][key]) == 1:
                    args['query'][key] = args['query'][key][0]
        else:
            (args['path'], args['query']) = (self.path, dict())
    
        payload = None
        payload_length = int(self.headers.get('Content-Length', failobj='0'))
        if payload_length:
            payload = self.rfile.read(payload_length).decode('UTF-8')
            try:
                payload = json.loads(payload)
                args['query'].update(payload)
            except ValueError as e:
                args['error_message'] = 'Payload is not valid JSON document'
                args['exception'] = e
                                                     
        return args
    
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

    def do_GET(self):
        params = self._parse_args()
        return self.do_HEAD(params=params, response=params)
 
    def do_POST(self):
        params = self._parse_args()
        if 'error_message' in params:
            self.send_error(code=400,
                            message=params['error_message'],
                            explain=str(params['exception']))
            self.log_error(str(params['exception']))
            return False
        else:
            return self.do_HEAD(params=params, response=params)
