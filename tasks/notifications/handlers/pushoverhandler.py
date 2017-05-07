#!/usr/bin/env python
# -*- coding: utf-8 -*-
from injector import inject

from services import PushoverService
from . import Handler


class PushoverHandler(Handler):
    @inject
    def __init__(self, pushover_service: PushoverService):
        self._pushover_service = pushover_service

    def handle(self, message: str):
        self._pushover_service.push(message)
