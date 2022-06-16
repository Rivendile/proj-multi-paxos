#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : kv.py
# Author            : Jing Mai <jingmai@pku.edu.cn>
# Date              : 06.12.2022
# Last Modified Date: 06.12.2022
# Last Modified By  : Jing Mai <jingmai@pku.edu.cn>

from typing import Tuple
import leveldb
import logging
from enum import IntEnum
from rwlock import RWLock, ReadLockGuard, WriteLockGuard

logger = logging.getLogger(__name__)


class KVClientRet(IntEnum):
    OK = 0
    SYS_FAIL = -1
    KEY_NOTEXIST = 1

class KVClient(object):
    def __init__(self) -> None:
        self.bHasInit = False
        self.oLevelDB = None
        self.oRWLock = RWLock()

    def Init(self, sDBPath: str) -> bool:
        if self.bHasInit:
            return True
        try:
            self.oLevelDB = leveldb.LevelDB(sDBPath, create_if_missing=True)
        except Exception as e:
            logger.error(f"open leveldb fail, db_path {sDBPath}, err {e}")
            return False
        self.bHasInit = True
        logger.info(f"OK, db_path {sDBPath}")
        return True

    def Get(self, sKey: str) -> Tuple[KVClientRet, bytes]:
        if not self.bHasInit:
            logger.error("not init yet")
            return KVClientRet.SYS_FAIL, None
        oGuard = ReadLockGuard(self.oRWLock)
        try:
            bValue = bytes(self.oLevelDB.Get(sKey.encode()))
        except KeyError as e:
            return KVClientRet.KEY_NOTEXIST, None
        except Exception as e:
            logger.error(f"LevelDB.Get fail, key {sKey}, err {e}")
            return KVClientRet.SYS_FAIL, None
        logger.info(f"Get OK, key {sKey}, value {bValue}")
        return KVClientRet.OK, bValue

    def Set(self, sKey: str, bValue: bytes) -> KVClientRet:
        if not self.bHasInit:
            logger.error("not init yet")
            return KVClientRet.SYS_FAIL, None, None
        oGuard = WriteLockGuard(self.oRWLock)
        try:
            self.oLevelDB.Put(sKey.encode(), bValue)
        except Exception as e:
            logger.error(f"LevelDB.Put fail, key {sKey}, err {e}")
            return KVClientRet.SYS_FAIL
        logger.info(f"Set OK, key {sKey}, value {bValue}")
        return KVClientRet.OK

    def Del(self, sKey: str) -> KVClientRet:
        if not self.bHasInit:
            logger.error("not init yet")
            return KVClientRet.SYS_FAIL
        eRet, bServerValue = self.Get(sKey)
        oGuard = WriteLockGuard(self.oRWLock)
        if eRet != KVClientRet.OK and eRet != KVClientRet.KEY_NOTEXIST:
            return eRet
        try:
            self.oLevelDB.Delete(sKey.encode())
        except Exception as e:
            logger.error(f"LevelDB.Delete fail, key {sKey}, err {e}")
            return KVClientRet.SYS_FAIL
        logger.info(f"Del OK, key {sKey}, value {bServerValue}")
        return KVClientRet.OK
