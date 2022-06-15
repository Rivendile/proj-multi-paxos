#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : sm.py
# Author            : Jing Mai <jingmai@pku.edu.cn>
# Date              : 06.12.2022
# Last Modified Date: 06.12.2022
# Last Modified By  : Jing Mai <jingmai@pku.edu.cn>
from abc import ABCMeta, abstractmethod

class StateMachine(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def SMID(self) -> int:
        """ State Machine ID """
        pass

    @abstractmethod
    def Execute(self, iInstanceIdx: int, sPaxosValue: str) -> bool:
        """ Return true means executes success. """
        pass