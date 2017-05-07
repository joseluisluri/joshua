#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import os

from injector import Injector

from config.constants import Constants
from services import LoggingService
from tasks import TaskManager, NotificationsTask, WhoisTask
from tasks.notifications.handlers import PushoverHandler
from tasks.whois.listeners import NotificationListener


class Joshua:
    def __init__(self):

        os.chdir()
        self._init_banner()

        self._injector = Injector()
        self._logger = self._injector.get(LoggingService).get_logger(type(self).__name__)

        # tasks
        self._logger.info('init tasks')
        self._task_manager = self._injector.get(TaskManager)
        self._init_tasks()
        self._task_manager.start()

        while True:
            time.sleep(1)

    @staticmethod
    def _init_banner():
        try:
            with open(Constants.BANNER_FILE) as file:
                print(file.read().format(Constants.NAME, Constants.VERSION))
        except Exception:
            print('Unable to print banner')

    def _init_tasks(self):

        # Notifications
        notifications_task = self._injector.get(NotificationsTask)
        pushover_handler = self._injector.get(PushoverHandler)
        notifications_task.handler = pushover_handler
        self._task_manager.add_task(notifications_task)

        # Who is
        whois_task = self._injector.get(WhoisTask)
        notification_listener = self._injector.get(NotificationListener)
        whois_task.add_listener(notification_listener)
        self._task_manager.add_task(whois_task)


if __name__ == '__main__':
    Joshua()
