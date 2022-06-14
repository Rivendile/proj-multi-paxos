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
from enum import Enum
from phxkv_pb2 import KVData
from rwlock import RWLock, ReadLockGuard, WriteLockGuard

logger = logging.getLogger(__name__)


class KVClientRet(Enum):
    OK = 0
    SYS_FAIL = -1
    KEY_NOTEXIST = 1
    KEY_VERSION_CONFLICT = -11

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

    def Get(self, sKey: str) -> Tuple[KVClientRet, bytes, int]:
        if not self.bHasInit:
            logger.error("not init yet")
            return KVClientRet.SYS_FAIL, None, None
        oGuard = ReadLockGuard(self.oRWLock)
        try:
            sBuffer = self.oLevelDB.Get(bytes(sKey, "utf-8"))
        except KeyError as e:
            logger.error(f"LevelDB.Get not found, key {sKey}")
            iVersion = 0
            return KVClientRet.KEY_NOTEXIST, None, iVersion
        except Exception as e:
            logger.error(f"LevelDB.Get fail, key {sKey}, err {e}")
            return KVClientRet.SYS_FAIL, None, None
        oData = KVData()
        try:
            oData.ParseFromString(sBuffer)
        except Exception as e:
            logger.error(f"parse fail, key {sKey}, err {e}")
            return KVClientRet.SYS_FAIL, None, None
        bValue = oData.value
        iVersion = oData.version
        bIsDeleted = oData.is_deleted
        if bIsDeleted:
            logger.error(f"LevelDB.Get key already deleted, key {sKey}")
            return KVClientRet.KEY_NOTEXIST, None, iVersion
        logger.info(f"Get OK, key {sKey}, value {bValue}, version {iVersion}")
        return KVClientRet.OK, bValue, iVersion

    def Set(self, sKey: str, bValue: bytes, iVersion: int) -> KVClientRet:
        if not self.bHasInit:
            logger.error("not init yet")
            return KVClientRet.SYS_FAIL, None, None
        oGuard = WriteLockGuard(self.oRWLock)
        eRet, _, iServerVersion = self.Get(sKey)
        if eRet != KVClientRet.OK and eRet != KVClientRet.KEY_NOTEXIST:
            return eRet
        if iVersion != iServerVersion:
            return KVClientRet.KEY_VERSION_CONFLICT
        iServerVersion += 1
        oData = KVData(value=bValue, version=iServerVersion, is_deleted=False)
        try:
            sBuffer = oData.SerializeToString()
        except Exception as e:
            logger.error(f"serialize fail, key {sKey}, err {e}")
            return KVClientRet.SYS_FAIL
        try:
            self.oLevelDB.Put(bytes(sKey, "utf-8"), sBuffer)
        except Exception as e:
            logger.error(f"LevelDB.Put fail, key {sKey}, err {e}")
            return KVClientRet.SYS_FAIL
        logger.info(f"Set OK, key {sKey}, value {bValue}, version {iServerVersion}")
        return KVClientRet.OK

    def Del(self, sKey: str, iVersion: int) -> KVClientRet:
        if not self.bHasInit:
            logger.error("not init yet")
            return KVClientRet.SYS_FAIL
        oGuard = WriteLockGuard(self.oRWLock)
        eRet, bServerValue, iServerVersion = self.Get(sKey)
        if eRet != KVClientRet.OK and eRet != KVClientRet.KEY_NOTEXIST:
            return eRet
        if iVersion != iServerVersion:
            return KVClientRet.KEY_VERSION_CONFLICT
        iServerVersion += 1
        oData = KVData(value=bServerValue, version=iServerVersion, is_deleted=True)
        try:
            sBuffer = oData.SerializeToString()
        except Exception as e:
            logger.error(f"serialize fail, key {sKey}, err {e}")
            return KVClientRet.SYS_FAIL
        try:
            self.oLevelDB.Put(bytes(sKey, "utf-8"), sBuffer)
        except Exception as e:
            logger.error(f"LevelDB.Put fail, key {sKey}, err {e}")
            return KVClientRet.SYS_FAIL
        logger.info(f"Del OK, key {sKey}, value {bServerValue}, version {iServerVersion}")
        return KVClientRet.OK
