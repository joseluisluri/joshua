#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from platform import system
from threading import Lock, Event

from injector import inject

from exceptions import ServiceException
from services import SettingsService, LoggingService, ShellService, NotificationsService
from .listeners import Listener
from .models import Device
from ..task import Task


class WhoisTask(Task):
    @inject
    def __init__(self, settings_service: SettingsService, shell_service: ShellService,
                 notifications_service: NotificationsService,
                 logging_service: LoggingService):
        self._settings = settings_service.get('whois')
        self._logger = logging_service.get_logger(type(self).__name__)
        self._notifications_service = notifications_service

        self._lock = Lock()
        self._lock_listeners = Lock()
        self._devices = []
        self._listeners = []
        self._active = False
        self._event = Event()
        self._interval = self._settings.interval
        self._shell_service = shell_service

    def start(self):
        self._active = True
        self._event.clear()
        for info in self._settings.devices:
            device = Device(info.name, info.ip)
            self._logger.trace('tracking ' + str(device))
            self._devices.append(device)

        self._logger.info('started')

    def run(self):
        try:
            while self._active:
                for device in self._devices:
                    old_status = device.status
                    device.status = self._check_status(device.ip)
                    device.timestamp = time.time()
                    self._logger.trace('Check name={} status={}'.format(device.name, device.status))

                    if old_status is not None and old_status != device.status:
                        with self._lock_listeners:
                            if device.status:
                                self._logger.trace('Device name={} arrive'.format(device.name))
                                for listener in self._listeners:
                                    listener.on_arrive(device)
                            else:
                                self._logger.trace('Device name={} leave'.format(device.name))
                                for listener in self._listeners:
                                    listener.on_leave(device)
                self._event.wait(self._interval)
        except ServiceException as e:
            self._logger.error('service error in runtime', e)

    def stop(self):
        self._event.set()
        self._active = False
        self._devices.clear()

    def add_listener(self, listener: Listener):
        with self._lock_listeners:
            self._listeners.append(listener)

    def remove_listener(self, listener: Listener):
        with self._lock_listeners:
            self._listeners.remove(listener)

    def _check_status(self, host: str) -> bool:
        if system().lower() == "windows":
            command = 'ping ' + host + ' -n 5 | find /i "(100%" /c'
        else:
            command = 'ping ' + host + ' -c 5 | grep "100%" | wc -l'

        return self._shell_service.execute(command) == "0"
