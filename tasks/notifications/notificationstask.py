#!/usr/bin/env python
# -*- coding: utf-8 -*-
from threading import Lock

import paho.mqtt.client as mqtt
from injector import inject

from exceptions.taskexception import TaskException
from services import LoggingService
from services.settingsservice import SettingsService
from tasks import Task
from .handlers import Handler


class NotificationsTask(Task):
    @inject
    def __init__(self, settings_service: SettingsService, logging_service: LoggingService):
        self._logger = logging_service.get_logger(type(self).__name__)
        self._config = settings_service.get('notifications')
        self._lock = Lock()
        self._lock_handler = Lock()
        self._handler: Handler = None
        try:
            self._client = mqtt.Client()
            self._logger.trace('init done')
        except Exception as e:
            self._logger.trace('init fails')

    def start(self):
        with self._lock:
            try:
                self._client.connect(self._config.host, self._config.port)
                self._client.subscribe(self._config.topic)
                self._client.on_message = self._on_notification
                self._logger.info('started')
            except Exception as e:
                self._logger.error('start failed', e)
                raise TaskException('unable to start task')

    def run(self):
        self._client.loop_start()

    def stop(self):
        with self._lock:
            self._client.loop_stop()
            self._client.disconnect()

    @property
    def handler(self):
        return self._handler

    @handler.setter
    def handler(self, handler: Handler):
        with self._lock_handler:
            self._handler = handler

    def _on_notification(self, client: mqtt.Client, userdata: any, message: any):
        with self._lock_handler:
            if self._handler is not None:
                self._handler.handle(str(message.payload, encoding='utf-8'))
