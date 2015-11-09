#!/usr/bin/python3
# -*- encoding: UTF-8 -*-

class CommandException(Exception):
    def __init__(self, message, explanation):
        super(CommandException, self).__init__(message)
        self.message = message
        self.explanation = explanation

class BotException(Exception):
    def __init__(self, message):
        super(BotException, self).__init__(message)
        self.message = message
        
class BotNotFoundException(BotException):
    def __init__(self, message):
        super(BotNotFoundException, self).__init__(message)
        self.message = message

class BotAddException(BotException):
    def __init__(self, message):
        super(BotAddException, self).__init__(message)
        self.message = message

class BotAlreadyExistsException(BotAddException):
    def __init__(self, message):
        super(BotAddExistsException, self).__init__(message)
        self.message = message
