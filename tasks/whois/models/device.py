#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time


class Device:
    def __init__(self, name, ip, status=None, timestamp: time=time.time()):
        self._name: str = name
        self._ip: str = ip
        self._status: bool = status
        self._timestamp: time = timestamp

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def ip(self) -> str:
        return self._ip

    @ip.setter
    def ip(self, ip: str):
        self._ip = ip

    @property
    def status(self) -> bool:
        return self._status

    @status.setter
    def status(self, status: bool):
        self._status = status

    @property
    def timestamp(self) -> time:
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp: time):
        self._timestamp = timestamp

    def __str__(self):
        return '[name={}, ip={}, status={}, timestamp={}]'.format(self._name, self._ip, self._status, self._timestamp)
