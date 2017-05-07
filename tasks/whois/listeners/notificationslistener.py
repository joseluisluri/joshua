#!/usr/bin/env python
# -*- coding: utf-8 -*-
from injector import inject

from services import SettingsService, LoggingService, NotificationsService
from . import Listener
from ..models import Device


class NotificationListener(Listener):
    @inject
    def __init__(self, settings_service: SettingsService, logging_service: LoggingService,
                 notifications_service: NotificationsService, ):
        self._topic = settings_service.get('notifications').topic
        self._settings = settings_service.get('whois')
        self._logger = logging_service.get_logger(type(self).__name__)
        self._notifications_service = notifications_service

    def on_arrive(self, device: Device):
        message = str(self._settings.on_arrive).format(device.name)
        self._notifications_service.push(self._topic, message)

    def on_leave(self, device: Device):
        message = str(self._settings.on_leave).format(device.name)
        self._notifications_service.push(self._topic, message)
