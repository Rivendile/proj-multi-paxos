from msvcrt import kbhit
from kv_sm import KVSM
import logging
from replicated_value import BaseReplicatedValue
from master_strategy import DedicatedMasterStrategyMixin
from resolution_strategy import ExponentialBackoffResolutionStrategyMixin
from sync_strategy import SimpleSynchronizationStrategyMixin
from messenger import Messenger
from utils.concurrent import PThread
from twisted.internet import reactor
from kv_enum import KVStatus, KVOperatorType
from phxkv_pb2 import PhxValue
from twisted.internet import reactor

logger = logging.getLogger(__name__)


class ReactorThread(PThread):
    def run(self):
        reactor.run()


def MakePaxosValue(sKey: str, sValue: str, iVersion: int, iOperator: int,
                   eOp: KVOperatorType) -> PhxValue:
    oPhxValue = PhxValue(
        key=sKey,
        value=sValue.encode(),
        version=iVersion,
        operator=int(eOp)
    )
    return oPhxValue.SerializeToString()


class PhxKV(object):
    def __init__(self, oMyUid, vecNodeList,
                 sKVDBPath: str, sPaxosLogPath: str, bUseMasterStrategy: bool):
        self.oMyUid = oMyUid
        self.vecNodeList = vecNodeList
        self.sKVDBPath = sKVDBPath
        self.sPaxosLogPath = sPaxosLogPath
        self.PaxosNode = None
        self.oKVSM = KVSM(sKVDBPath)
        self.bUseMasterStrategy = bUseMasterStrategy
        self.oReplicatedValue = None
        self.oMessager = None
        self.oReactorThread = ReactorThread()

    def InitPaxos(self) -> int:
        if not self.oKVSM.Init():
            return -1
        if self.bUseMasterStrategy:
            class ReplicatedValue(DedicatedMasterStrategyMixin, ExponentialBackoffResolutionStrategyMixin, SimpleSynchronizationStrategyMixin, BaseReplicatedValue):
                '''
                Mixes the dedicated master, resolution, and synchronization strategies into the base class
                '''
        else:
            class ReplicatedValue(ExponentialBackoffResolutionStrategyMixin, SimpleSynchronizationStrategyMixin, BaseReplicatedValue):
                '''
                Mixes just the resolution and synchronization strategies into the base class
                '''
        self.oReplicatedValue = ReplicatedValue(self.oMyNode, self.vecNodeList.keys(), self.sPaxosLogPath, self.oKVSM)
        self.oMessager = Messenger(self.oMyNode, self.vecNodeList, self.oReplicatedValue)
        return 0

    def RunPaxos(self):
        self.oReactorThread.start()

    def KVPropose(self, sPaxosValue: str) -> int:
        self.oReplicatedValue.propose_update(sPaxosValue)

    def Put(self, sKey: str, sValue: str, iVersion: int) -> KVStatus:
        sPaxosValue = MakePaxosValue(sKey, sValue, iVersion, KVOperatorType.WRITE)
        self.KVPropose(sPaxosValue)

    def GetLocal(self, sKey: str) -> KVStatus:
        eStatus, sValue, iVersion = self.oKVSM.Get(sKey)
        return eStatus, sValue, iVersion

    def Delete(self, sKey: str, iVersion: int) -> KVStatus:
        sPaxosValue = MakePaxosValue(sKey, "", iVersion, KVOperatorType.DELETE)
        self.KVPropose(sPaxosValue)
