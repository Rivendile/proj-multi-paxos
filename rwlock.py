import threading
from threading import Lock, Condition


class RWLock(object):
    def __init__(self):
        self.oLock = Lock()
        self.oRCond = Condition(self.oLock)
        self.oWCond = Condition(self.oLock)
        self.iRWaiter = 0  # num of threads waiting for read
        self.iWWaiter = 0  # num of threads waiting for write
        # Positive: num of reading threads; Negative(only -1): num of writing threads (only at most one writer)
        self.iState = 0
        self.vecOwners = []  # list of threads that own the lock
        self.bWriteFirst = True  # True: write first; False: read first

    def WriteAcquire(self, blocking=True):
        iMe = threading.get_ident()
        with self.oLock:
            while not self._WriteAcquire(iMe):
                if not blocking:
                    return False
                self.iWWaiter += 1
                self.oWCond.wait()
                self.iWWaiter -= 1
        return True

    def _WriteAcquire(self, iMe):
        if self.iState == 0 or (self.iState < 0 and iMe in self.vecOwners):
            self.iState -= 1
            self.vecOwners.append(iMe)
            return True
        if self.iState > 0 and iMe in self.vecOwners:
            raise RuntimeError('cannot recursively wrlock a rdlocked lock')
        return False

    def ReadAcquire(self, blocking=True):
        iMe = threading.get_ident()
        with self.oLock:
            while not self._ReadAcquire(iMe):
                if not blocking:
                    return False
                self.iRWaiter += 1
                self.oRCond.wait()
                self.iRWaiter -= 1
        return True

    def _ReadAcquire(self, iMe):
        if self.iState < 0:
            return False
        if not self.iWWaiter:
            ok = True
        else:
            ok = iMe in self.vecOwners
        if ok or not self.bWriteFirst:
            self.iState += 1
            self.vecOwners.append(iMe)
            return True
        return False

    def Unlock(self):
        iMe = threading.get_ident()
        with self.oLock:
            try:
                self.vecOwners.remove(iMe)
            except ValueError:
                raise RuntimeError('cannot release un-acquired lock')

            if self.iState > 0:
                self.iState -= 1
            else:
                self.iState += 1
            if not self.iState:
                if self.iWWaiter and self.bWriteFirst:
                    self.oWCond.notify()
                elif self.iRWaiter:
                    self.oRCond.notify_all()
                elif self.iWWaiter:
                    self.oWCond.notify()

    ReadRelease = Unlock
    WriteRelease = Unlock


class ReadLockGuard(object):
    def __init__(self, oRWLock):
        self.oRWLock = oRWLock
        self.oRWLock.ReadAcquire()

    def __del__(self):
        self.oRWLock.ReadRelease()

class WriteLockGuard(object):
    def __init__(self, oRWLock):
        self.oRWLock = oRWLock
        self.oRWLock.WriteAcquire()

    def __del__(self):
        self.oRWLock.WriteRelease()