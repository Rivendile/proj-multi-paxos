#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : kvsm.py
# Author            : Jing Mai <jingmai@pku.edu.cn>
# Date              : 06.12.2022
# Last Modified Date: 06.12.2022
# Last Modified By  : Jing Mai <jingmai@pku.edu.cn>

from sm import StateMachine
from kv_client import KVClient
import logging

logger = logging.getLogger(__name__)


class KVSM(StateMachine):
    def __init__(self, sDBPath: str):
        super(KVSM, self).__init__()
        self.sDBPath = sDBPath
        self.oKVClient = KVClient()

    def Init(self) -> bool:
        bSucc = self.oKVClient.Init(self.sDBPath)
        if not bSucc:
            logger.error(f"KVClient.Init fail, db_path {self.sDBPath}")
            return False
        return True

    def Execute(self, iInstanceIdx: int, sPaxosValue: str) -> bool:
        pass