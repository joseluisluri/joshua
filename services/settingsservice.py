#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io

import yaml
from attrdict import AttrDict
from injector import singleton

from config.constants import Constants
from exceptions import ServiceException


class SettingsService:
    @singleton
    def __init__(self):
        try:
            with io.open(Constants.CONFIG_FILE, 'r', encoding='utf8') as stream:
                self._settings = yaml.load(stream)
        except:
            raise ServiceException('Unable to load settings')

    def get(self, section: str) -> any:
        return AttrDict(self._settings[section])
