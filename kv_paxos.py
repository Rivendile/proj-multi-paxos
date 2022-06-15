from kv_sm import KVSM
import logging
from replicated_value import BaseReplicatedValue
from master_strategy import DedicatedMasterStrategyMixin
from resolution_strategy import ExponentialBackoffResolutionStrategyMixin
from sync_strategy import SimpleSynchronizationStrategyMixin
from messenger import Messenger
from utils.concurrent import PThread
from twisted.internet import reactor

logger = logging.getLogger(__name__)

class ReactorThread(PThread):
    def run(self):
        reactor.run()
        
class PhxKV(object):
    def __init__(self, oMyNode, vecNodeList,
                 sKVDBPath: str, sPaxosLogPath: str, bUseMasterStrategy: bool):
        self.oMyNode = oMyNode
        self.vecNodeList = vecNodeList
        self.sKVDBPath = sKVDBPath
        self.sPaxosLogPath = sPaxosLogPath
        self.PaxosNode = None
        self.oKVSM = KVSM(sKVDBPath)
        self.bUseMasterStrategy = bUseMasterStrategy
        self.oReplicatedValue = None
        self.oMessager = None
        self.oReactorThread = ReactorThread()

    def RunPaxos(self) -> int:
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
        self.oReactorThread.start()
        return 0

    def KVPropose(self, sKey: str, sPaxosValue: str) -> int:
        iGroupIdx = self.GetGroupIdx(sKey)
