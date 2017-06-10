#!/usr/bin/env python
# -*- coding: utf-8 -*-
from enum import Enum
import time
from injector import inject, singleton

from services.settingsservice import SettingsService


class Level(Enum):
    TRACE = 1
    INFO = 2
    WARNING = 3
    ERROR = 4


class Logger:
    def __init__(self, settings: any, name: str):
        self._name = name
        self._settings = settings
        self._level = Level[settings.level]

    def trace(self, message: str, exception: Exception = None):
        self._log(Level.TRACE, message)

    def info(self, message: str, exception: Exception = None):
        self._log(Level.INFO, message)

    def warning(self, message: str, exception: Exception = None):
        self._log(Level.WARNING, message)

    def error(self, message: str, exception: Exception = None):
        self._log(Level.ERROR, message)

    def _log(self, level: Level, message: str):
        info = {'name': self._name, 'date': time.strftime(self._settings.date_format), 'level': level.name,
                'message': message}
        #if level.value >= self._level.value:
        print(self._settings.format.format(**info))


class LoggingService:
    @singleton
    @inject
    def __init__(self, settings_service: SettingsService):
        self._settings = settings_service.get('logging')

    def get_logger(self, name: str) -> Logger:
        return Logger(self._settings, name)
