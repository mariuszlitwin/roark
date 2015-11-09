#!/usr/bin/python3
# -*- encoding: UTF-8 -*-

import medium.exceptions 

class dummy:      
    def query_bot(self,
                  path,
                  query):
        if path in self.roark_status['registered_bot']:
            return self.roark_status['registered_bot'][path].request(query)
        else:
            raise medium.exceptions.BotNotFoundException('No bot registered under {path}'.format(path=path))
            return None
