#!/usr/bin/python3
# -*- encoding: UTF-8 -*-

import medium.exceptions 

class dummy:
    def __init__(self, registered_bot=None):
        global roark_status
        if registered_bot == None:
            registered_bot = roark_status['registered_bot']
        else:
            self._registered_bot = registered_bot

    def register_bot(self,
                     bot,
                     path):
        if path in self._registered_bot:
            raise medium.exceptions.BotAlreadyExistsException('There is another bot registered under that path')
        self._registered_bot['path'] = bot
        
    def query_bot(self,
                  path,
                  query):
        if path in self._registered_bot:
            return self._registered_bot.request(query)
        else:
            raise medium.exceptions.BotNotFoundException('No bot registered under {path}'.format(path=path))
            return None
