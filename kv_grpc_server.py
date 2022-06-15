from phxkv_pb2_grpc import PhxKVServicer
from phxkv_pb2 import PhxKVResponse
from kv_paxos import PhxKV
import logging
from kv_enum import KVStatus

logger = logging.getLogger(__name__)


class PhxKVServicerImpl(PhxKVServicer):
    def __init__(
        self,
        oMyUid,
        vecNodeList,
        sKVDBPath: str,
        sPaxosLogPath: str,
        bUseMasterStrategy: bool,
    ):
        super(PhxKVServicerImpl, self).__init__()
        self.oPhxKV = PhxKV(
            oMyUid, vecNodeList, sKVDBPath, sPaxosLogPath, bUseMasterStrategy
        )

    def Init(self):
        return self.oPhxKV.InitPaxos()

    def Put(self, request, context) -> PhxKVResponse:
        eStatus = self.oPhxKV.Put(request.key, request.value)
        oResponse = PhxKVResponse(ret=eStatus)
        logging.info(f"ret {eStatus}, key {request.key}, value {request.value}")
        return oResponse

    def GetLocal(self, request, context) -> PhxKVResponse:
        eStatus, bValue = self.oPhxKV.GetLocal(request.key)
        logging.info(
            f"ret {eStatus}, key {request.key}, value {bValue}"
        )
        oResponse = PhxKVResponse(ret=eStatus, value=bValue)
        return oResponse

    def GetGlobal(self, request, context) -> PhxKVResponse:
        # FIXME(Jing Mai): If I am not the master node for the query key, I should return the master node id to the client instead of the value.
        return self.GetLocal(request, context)

    def Delete(self, request, context) -> PhxKVResponse:
        eStatus = self.oPhxKV.Delete(request.key)
        oResponse = PhxKVResponse(ret=eStatus)
        logging.info(f"ret {eStatus}, key {request.key}")
        return oResponse
