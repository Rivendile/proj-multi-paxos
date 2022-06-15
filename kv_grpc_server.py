from phxkv_pb2_grpc import PhxKVServicer
from phxkv_pb2 import PhxKVResponse
from kv_paxos import PhxKV
import logging
from kv_enum import KVStatus

logger = logging.getLogger(__name__)


class PhxKVServicerImpl(PhxKVServicer):
    def __init__(self,
                 oMynode,
                 vecNodeList,
                 sKVDBPath: str,
                 sPaxosLogPath: str):
        super(PhxKVServicerImpl, self).__init__()
        self.oPhxKV = PhxKV(oMynode, vecNodeList, sKVDBPath, sPaxosLogPath)

    def Init(self):
        return self.oPhxKV.InitPaxos()

    def Start(self):
        return self.oPhxKV.RunPaxos()
    
    def Put(self, request, context) -> PhxKVResponse:
        eStatus = self.oPhxKV.Put(request.key, request.value, request.version)
        oResponse = PhxKVResponse(ret=eStatus)
        logging.info(f"ret {eStatus}, key {request.key}, value {request.value}, version {request.version}")
        return oResponse

    def GetLocal(self, request, context) -> PhxKVResponse:
        eStatus, sValue, iVersion = self.oPhxKV.GetLocal(request.key)
        oResponse = PhxKVResponse(ret=eStatus)
        if eStatus == KVStatus.SUCC:
            oResponse.data.value = sValue
            oResponse.data.version = iVersion
        elif eStatus == KVStatus.KEY_NOTEXIST:
            oResponse.data.is_deleted = True
            oResponse.data.version = iVersion
        logging.info(f"ret {eStatus}, key {request.key}, value {sValue}, version {iVersion}")
        return oResponse

    def GetGlobal(self, request, context) -> PhxKVResponse:
        # FIXME(Jing Mai): If I am not the master node for the query key, I should return the master node id to the client instead of the value.
        return self.GetLocal(request, context)

    def Delete(self, request, context) -> PhxKVResponse:
        eStatus = self.oPhxKV.Delete(request.key, request.version)
        oResponse = PhxKVResponse(ret=eStatus)
        logging.info(f"ret {eStatus}, key {request.key}, version {request.version}")
        return oResponse
