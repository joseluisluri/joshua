#!/usr/bin/env python
# -*- coding: utf-8 -*-
from abc import abstractmethod, ABCMeta


class Handler:
    __metaclass__ = ABCMeta

    @abstractmethod
    def handle(self, message: str):
        pass
