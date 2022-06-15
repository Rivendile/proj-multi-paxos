from threading import Thread
from abc import ABCMeta, abstractmethod

class PThread(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self._thread = None

    def start(self):
        self._thread = Thread(target=self.run)
        self._thread.start()

    def join(self):
        self._thread.join()

    @property
    def ident(self):
        return self._thread.ident
        
    @abstractmethod
    def run(self):
        pass