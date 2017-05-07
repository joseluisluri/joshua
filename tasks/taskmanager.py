#!/usr/bin/env python
# -*- coding: utf-8 -*-
from concurrent.futures import ThreadPoolExecutor

from injector import inject

from exceptions import ServiceException
from exceptions.taskexception import TaskException
from services import LoggingService
from services import SettingsService
from . import Task


class TaskManager:
    @inject
    def __init__(self, settings_service: SettingsService, logging_service: LoggingService):
        self._tasks = []
        self._logger = logging_service.get_logger(type(self).__name__)

        try:
            self._settings = settings_service.get('taskmanager')
            self._task_pool = ThreadPoolExecutor(self._settings.pool_size)
        except ServiceException as e:
            raise TaskException('Unable to get settings', e)
        except ValueError as e:
            raise TaskException('Invalid pool size', e)

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
