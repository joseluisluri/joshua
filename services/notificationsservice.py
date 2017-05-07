#!/usr/bin/env python
# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
from injector import singleton, inject

from exceptions import ServiceException
from services import SettingsService, LoggingService


class NotificationsService:
    @singleton
    @inject
    def __init__(self, settings_service: SettingsService, logging_service: LoggingService):
        self._settings = settings_service.get('notifications')
        self._logger = logging_service.get_logger(type(self).__name__)
        try:
            self._client = mqtt.Client()
            self._logger.trace('init done')
        except Exception as e:
            self._logger.trace('init fails')
            raise ServiceException('Unable to initialize service', e)


    def push(self, topic: str, message: str):
        try:
            self._client.connect(self._settings.host, self._settings.port)
            self._client.publish(topic, message)
            self._client.disconnect()
            self._logger.trace('notification sent. topic={}, message={}'.format(topic, message))
        except Exception as e:
            self._logger.trace('notification could not be sent')
            raise ServiceException('Unable to sent notification', e)
