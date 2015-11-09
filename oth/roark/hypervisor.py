#!/usr/bin/python3
# -*- encoding: UTF-8 -*-

import bot.dummy
import medium.dummy
import oth.roark.exceptions

def add_bot(medium_class, bot_obj, path):
    assert isinstance(bot_obj, bot.dummy.dummy), "bot_obj must be object of bot"
    assert issubclass(medium_class, medium.dummy.dummy), "medium_class must be class of medium"
    
    if not medium_class.bot_list:
        medium_class.bot_list = dict()
        
    if path in medium_class.bot_list:
        raise oth.roark.exceptions.BotAlreadyExistsException('{path} bot-path already registered'.format(path=path))
    else:
        medium_class.bot_list[path] = bot_obj
        
def add_api_key(medium_class, api_key):
    assert issubclass(medium_class, medium.dummy.dummy), "medium_class must be class of medium"
    
    medium_class.api_key = api_key
