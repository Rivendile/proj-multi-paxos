import logging
from replicated_value import BaseReplicatedValue
from kv_sm import KVSM
from master_strategy import DedicatedMasterStrategyMixin
from resolution_strategy import ExponentialBackoffResolutionStrategyMixin
from sync_strategy import SimpleSynchronizationStrategyMixin
from messenger import Messenger
from utils.concurrent import PThread
from twisted.internet import reactor
from kv_enum import KVStatus, KVOperatorType
from phxkv_pb2 import PhxValue
from twisted.internet import reactor
from typing import Tuple

logger = logging.getLogger(__name__)


def MakePaxosValue(sKey: str, bValue: bytes, eOp: KVOperatorType) -> PhxValue:
    oPhxValue = PhxValue(key=sKey, value=bValue, operator=int(eOp))
    return oPhxValue.SerializeToString().decode()


class PhxKV(object):
    def __init__(
        self,
        oMyUid,
        vecNodeList,
        sKVDBPath: str,
        sPaxosLogPath: str,
        bUseMasterStrategy: bool,
    ):
        self.oMyUid = oMyUid
        self.vecNodeList = vecNodeList
        self.sKVDBPath = sKVDBPath
        self.sPaxosLogPath = sPaxosLogPath
        self.PaxosNode = None
        self.oKVSM = KVSM(sKVDBPath)
        self.bUseMasterStrategy = bUseMasterStrategy
        self.oReplicatedValue = None
        self.oMessager = None

    def InitPaxos(self) -> int:
        if not self.oKVSM.Init():
            return -1
        if self.bUseMasterStrategy:

            class ReplicatedValue(
                DedicatedMasterStrategyMixin,
                ExponentialBackoffResolutionStrategyMixin,
                SimpleSynchronizationStrategyMixin,
                BaseReplicatedValue,
            ):
                """
                Mixes the dedicated master, resolution, and synchronization strategies into the base class
                """

        else:

            class ReplicatedValue(
                ExponentialBackoffResolutionStrategyMixin,
                SimpleSynchronizationStrategyMixin,
                BaseReplicatedValue,
            ):
                """
                Mixes just the resolution and synchronization strategies into the base class
                """

        self.oReplicatedValue = ReplicatedValue(
            self.oMyUid, self.vecNodeList.keys(), self.sPaxosLogPath, self.oKVSM
        )
        self.oMessager = Messenger(self.oMyUid, self.vecNodeList, self.oReplicatedValue)
        return 0

    def KVPropose(self, sPaxosValue: str) -> int:
        self.oReplicatedValue.propose_update(sPaxosValue)

    def Put(self, sKey: str, bValue: bytes) -> KVStatus:
        sPaxosValue = MakePaxosValue(sKey, bValue, KVOperatorType.WRITE)
        self.KVPropose(sPaxosValue)
        return KVStatus.SUCC

    def GetLocal(self, sKey: str) -> Tuple[KVStatus, bytes]:
        eStatus, sValue = self.oKVSM.Get(sKey)
        return eStatus, sValue

    def Delete(self, sKey: str) -> KVStatus:
        sPaxosValue = MakePaxosValue(sKey, "".encode(), KVOperatorType.DELETE)
        self.KVPropose(sPaxosValue)
        return KVStatus.SUCC
