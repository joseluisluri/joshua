#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pushover
from injector import inject, singleton

from exceptions import ServiceException
from services import SettingsService, LoggingService


class PushoverService:
    @singleton
    @inject
    def __init__(self, settings_service: SettingsService, logging_service: LoggingService):
        self._logger = logging_service.get_logger(type(self).__name__)
        self._settings = settings_service.get('pushover')
        try:
            pushover.init(self._settings.token, self._settings.sound)
            self._client = pushover.Client(self._settings.userkey)
            self._logger.trace('init done')
        except Exception as e:
            self._logger.trace('init fails')
            raise ServiceException('Unable to init pushover client', e)

    def push(self, message: str, title: str="", sound: str=None):
        try:
            sound = self._settings.sound if sound is None else sound
            self._client.send_message(message, title=title, sound=sound)
            self._logger.trace('message sent to Pushover')
        except Exception as e:
            self._logger.trace('message could not be sent to Pushover')
            raise ServiceException("Unable to push message", e)
