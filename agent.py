#!/usr/bin/python3
# -*- encoding: UTF-8 -*-

if __name__ == '__main__':
    from http.server import HTTPServer
    from medium.RestAPI import RestAPIHandler
    server = HTTPServer(('localhost', 8080), RestAPIHandler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()
