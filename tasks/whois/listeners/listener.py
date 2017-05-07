#!/usr/bin/env python
# -*- coding: utf-8 -*-
from abc import abstractmethod, ABCMeta
from ..models import Device


class Listener:
    __metaclass__ = ABCMeta

    @abstractmethod
    def on_arrive(self, profile: Device):
        pass

    @abstractmethod
    def on_leave(self, profile: Device):
        pass
