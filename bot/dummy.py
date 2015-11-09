#!/usr/bin/python3
# -*- encoding: UTF-8 -*-

class dummy:
    def __init__(self):
        pass
        
    def request(self, path, query):
        query['path'] = path
        return query
