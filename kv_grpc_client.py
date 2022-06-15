from typing import Tuple
import phxkv_pb2
import phxkv_pb2_grpc
import grpc
from kv_enum import KVOperatorType, KVStatus
import logging

logger = logging.getLogger(__name__)


class PhxKVClient(object):
    def __init__(self, oChannel: grpc.Channel):
        self.oStub = phxkv_pb2_grpc.PhxKVStub(oChannel)

    def Put(self, sKey: str, bValue: bytes) -> KVStatus:
        oRequest = phxkv_pb2.PhxKVRequest(key=sKey, value=bValue)
        oRequest.operator = int(KVOperatorType.WRITE)
        try:
            oResponse = self.oStub.Put(oRequest)
        except grpc.RpcError as e:
            logger.error(f"RpcError {e}")
            return KVStatus.FAIL
        return oResponse.ret

    def GetLocal(self, sKey: str) -> Tuple[KVStatus, bytes]:
        oRequest = phxkv_pb2.PhxKVRequest(key=sKey)
        oRequest.operator = int(KVOperatorType.READ)
        try:
            oResponse = self.oStub.GetLocal(oRequest)
        except grpc.RpcError as e:
            logger.error(f"RpcError {e}")
            return KVStatus.FAIL, None, None
        return oResponse.ret, oResponse.value

    def GetGlobal(self, sKey: str) -> Tuple[KVStatus, bytes]:
        oRequest = phxkv_pb2.PhxKVRequest(key=sKey)
        oRequest.operator = int(KVOperatorType.READ)
        try:
            oResponse = self.oStub.GetGlobal(oRequest)
        except grpc.RpcError as e:
            logger.error(f"RpcError {e}")
            return KVStatus.FAIL, None, None
        return oResponse.ret, oResponse.value

    def Delete(self, sKey: str) -> KVStatus:
        oRequest = phxkv_pb2.PhxKVRequest(key=sKey)
        oRequest.operator = int(KVOperatorType.DELETE)
        try:
            oResponse = self.oStub.Delete(oRequest)
        except grpc.RpcError as e:
            logger.error(f"RpcError {e}")
            return KVStatus.FAIL
        return oResponse.ret
