#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io

import yaml
from attrdict import AttrDict
from injector import singleton

from config.constants import CONFIG_FILE
from exceptions import ServiceException
from services import Service


class SettingsService(Service):
    @singleton
    def __init__(self):
        try:
            with io.open(CONFIG_FILE, 'r', encoding='utf8') as stream:
                self._settings = yaml.load(stream)
        except:
            raise ServiceException('Unable to load settings')

    def get(self, section: str) -> any:
        try:
            return AttrDict(self._settings[section])
        except KeyError:
            raise ServiceException('Undefined section ' + section)
