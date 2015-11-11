#!/usr/bin/python3
# -*- encoding: UTF-8 -*-

import bot.dummy
import oth.roark.exceptions

class fs(bot.dummy.dummy):
    def request(self, path, query):
        response = None
        try:
            if len(path) == 1 and query['command'] == 'GET' and \
               'uri' in query:
                with open(query['uri'], 'r') as f:
                    response = {'uri': query['uri'],
                                'content': f.read()}
            else:
                raise oth.roark.exceptions.CommandException("Invalid command.", None)
        except OSError as e:
            raise oth.roark.exceptions.CommandException("File cannot be opened.", str(e))
        return response
