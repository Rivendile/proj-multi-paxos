#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : kvsm.py
# Author            : Jing Mai <jingmai@pku.edu.cn>
# Date              : 06.12.2022
# Last Modified Date: 06.12.2022
# Last Modified By  : Jing Mai <jingmai@pku.edu.cn>

from sm import StateMachine
from kv_client import KVClient, KVClientRet
import logging
from typing import Tuple
from phxkv_pb2 import PhxValue
from kv_enum import KVOperatorType, KVStatus

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
    
    def Get(self, sKey: str) -> Tuple[KVStatus, bytes]:
        oRet, bValue = self.oKVClient.Get(sKey)
        if oRet == KVClientRet.OK:
            return KVStatus.SUCC, bValue
        elif oRet == KVClientRet.KEY_NOTEXIST:
            return KVStatus.KEY_NOTEXIST, bValue
        elif oRet == KVClientRet.SYS_FAIL:
            return KVStatus.SYS_FAIL, bValue
    
    def Execute(self, iInstanceIdx: int, sPaxosValue: str):
        oPhxValue = PhxValue()
        oPhxValue.ParseFromString(sPaxosValue.encode())
        sKey = oPhxValue.key
        bValue = oPhxValue.value
        eOp = KVOperatorType(oPhxValue.operator)
        if eOp == KVOperatorType.READ:
            self.oKVClient.Get(sKey)
        elif eOp == KVOperatorType.WRITE:
            self.oKVClient.Set(sKey, bValue)
        elif eOp == KVOperatorType.DELETE:
            self.oKVClient.Del(sKey)
        