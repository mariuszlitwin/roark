#!/usr/bin/python3
# -*- encoding: UTF-8 -*-

import shlex
import subprocess

import bot.dummy
import oth.roark.exceptions

class process(bot.dummy.dummy):
    def __init__(self):
        self.tracked_process = dict()

    def request(self, path, query):
        response = None
        try:
            if len(path) == 1 and query['command'] == 'POST' and 'command_line' in query:
                command_line = shlex.split(query['command_line'])
                p = subprocess.Popen(command_line,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
                self.tracked_process[p.pid] = p
                
                response = {'pid': p.pid}
            elif len(path) == 1 and query['command'] == 'GET':
                
                response = {'process': dict(
                                            zip(
                                                self.tracked_process.keys(),
                                                (' '.join(val.args) for val in self.tracked_process.values())
                                               )
                                           )}
            elif len(path) == 2 and query['command'] == 'GET':
                pid = int(path[1])
                (outs, errs) = self.tracked_process[pid].communicate(timeout=1)
                response = {'pid': pid,
                            'stdout': outs,
                            'stderr': errs,
                            'returncode': self.tracked_process[pid].returncode}
            elif len(path) == 2 and query['command'] == 'PUT':
                pid = int(path[1])
                if 'signal' in query:
                    self.tracked_process[pid].send_signal(query['signal'])
                (outs, errs) = self.tracked_process[pid].communicate(input=query.get('input', 
                                                                                     None),
                                                                         timeout=1)
                response = {'pid': pid,
                            'stdout': outs,
                            'stderr': errs,
                            'returncode': self.tracked_process[pid].returncode}
            elif len(path) == 2 and query['command'] == 'DELETE':
                pid = int(path[1])
                self.tracked_process[pid].terminate()
                response = {'pid': pid,
                            'acknowledge': True}
            else:
                raise oth.roark.exceptions.CommandException("Invalid command.", None)
        except KeyError as e:
            raise oth.roark.exceptions.CommandException("PID {pid} not registered.".format(pid=path[1]), str(e))
        except subprocess.TimeoutExpired as e:
            raise oth.roark.exceptions.CommandException("PID {pid} hasn't responded in 1 second.".format(pid=path[1]), str(e))
        else:
            return response
