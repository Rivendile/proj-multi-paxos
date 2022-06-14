from typing import Tuple
import phxkv_pb2
import phxkv_pb2_grpc
import grpc
from kv_enum import KVOperatorType, KVStatus
import logging

logger = logging.getLogger(__name__)


class PhxKVClient(object):
    def __init__(self, oChannel: grpc.Channel):
        self.oStub = phxkv_pb2_grpc.PhxKVServerStub(oChannel)

    def Put(self, sKey: str, sValue: str, iVersion: int) -> KVStatus:
        oRequest = phxkv_pb2.PhxKVRequest(key=sKey, value=sValue, version=iVersion)
        oRequest.opeartor = KVOperatorType.WRITE
        try:
            oResponse = self.oStub.Put(oRequest)
        except grpc.RpcError as e:
            logger.error(f"RpcError {e}")
            return KVStatus.FAIL
        return oResponse.ret

    def GetLocal(self, sKey: str) -> Tuple[KVStatus, bytes, int]:
        oRequest = phxkv_pb2.PhxKVRequest(key=sKey)
        oRequest.operator = KVOperatorType.READ
        try:
            oResponse = self.oStub.GetLocal(oRequest)
        except grpc.RpcError as e:
            logger.error(f"RpcError {e}")
            return KVStatus.FAIL, None, None
        return oResponse.ret, oResponse.data.value, oResponse.data.version

    def GetLocal(self, sKey: str, iMinVersion: int) -> Tuple[KVStatus, bytes, int]:
        eStatus, sValue, iVersion = self.GetLocal(sKey)
        if eStatus == KVStatus.SUCC:
            if iVersion is not None and iVersion < iMinVersion:
                eStatus = KVStatus.VERSION_NOTEXIST
        return eStatus, sValue, iVersion

    def GetGlobal(self, sKey: str) -> Tuple[KVStatus, bytes, int]:
        oRequest = phxkv_pb2.PhxKVRequest(key=sKey)
        oRequest.operator = KVOperatorType.READ
        try:
            oResponse = self.oStub.GetGlobal(oRequest)
        except grpc.RpcError as e:
            logger.error(f"RpcError {e}")
            return KVStatus.FAIL, None, None
        return oResponse.ret, oResponse.data.value, oResponse.data.version

    def Delete(self, sKey: str, iVersion: int) -> KVStatus:
        oRequest = phxkv_pb2.PhxKVRequest(key=sKey, version=iVersion)
        oRequest.operator = KVOperatorType.DELETE
        try:
            oResponse = self.oStub.Delete(oRequest)
        except grpc.RpcError as e:
            logger.error(f"RpcError {e}")
            return KVStatus.FAIL
        return oResponse.ret
