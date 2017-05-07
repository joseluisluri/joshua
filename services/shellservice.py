#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess

from injector import singleton

from exceptions import ServiceException


class ShellService:
    @singleton
    def execute(self, command: str):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        out, error = process.communicate()
        if error is None:
            return out.decode('utf-8').strip()
        else:
            raise ServiceException('Error while executing command ' + command)
