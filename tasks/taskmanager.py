#!/usr/bin/env python
# -*- coding: utf-8 -*-
from concurrent.futures import ThreadPoolExecutor

from injector import inject

from exceptions import ServiceException, JoshuaException
from services.loggingservice import LoggingService
from services.settingsservice import SettingsService
from . import Task


class TaskManager:
    @inject
    def __init__(self, settings_service: SettingsService, logging_service: LoggingService):
        self._tasks = []
        self._logger = logging_service.get_logger(type(self).__name__)

        try:
            self._settings = settings_service.get('joshua')
            self._task_pool = ThreadPoolExecutor(self._settings.pool_size)
        except ServiceException as e:
            raise JoshuaException('Unable to get settings', e)
        except ValueError as e:
            raise JoshuaException('Invalid pool size', e)

    def add_task(self, task: Task):
        self._tasks.append(task)

    def remove_task(self, task: Task):
        self._tasks.remove(task)

    def start(self):
        for task in self._tasks:
            task.start()
            self._task_pool.submit(task.run)

    def stop(self):
        for task in self._tasks:
            task.stop()
        self._task_pool.shutdown(True)

    def stop_now(self):
        self._task_pool.shutdown(False)
