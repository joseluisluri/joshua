#!/usr/bin/env python
# -*- coding: utf-8 -*-
import inspect
import signal
import traceback
from os import listdir
from os.path import isdir, join
from importlib import import_module
from injector import Injector
from inspect import getmembers

from config.constants import TASKS_DIR, TASKS_PATTERN, BANNER_FILE, NAME, VERSION
from exceptions import ServiceException, TaskException, JoshuaException
from services.loggingservice import LoggingService
from tasks import TaskManager, Task


class Joshua:
    def __init__(self):
        try:
            self._init_banner()
            self._injector = Injector()
            self._logger = self._injector.get(LoggingService).get_logger(type(self).__name__)

            self._task_manager = self._injector.get(TaskManager)
            self._init_load_tasks()
            self._task_manager.start()
            input()
            self._task_manager.stop()
        except ImportError as e:
            print('Unable to import task', e)
        except ServiceException as e:
            print('Service failed: ' + str(e))
        except TaskException as e:
            print('Task failed: ' + str(e))
        except JoshuaException as e:
            print('Joshua internal error: ' + str(e))
            traceback.print_stack()

    @staticmethod
    def _init_banner():
        try:
            with open(BANNER_FILE) as file:
                print(file.read().format(NAME, VERSION))
        except Exception:
            raise JoshuaException('Unable to print banner')

    def _init_load_tasks(self):
        for task in listdir(TASKS_DIR):
            if not task.startswith('__') and isdir(join(TASKS_DIR, task)):
                module_name = TASKS_PATTERN.format(task)
                dynamic_module = import_module(module_name, package=__package__)

                for member in getmembers(dynamic_module, inspect.isclass):
                    name, clazz = member
                    if issubclass(clazz, Task):
                        self._logger.trace('task {} added'.format(name))
                        self._task_manager.add_task(self._injector.get(clazz))


if __name__ == '__main__':
    Joshua()
