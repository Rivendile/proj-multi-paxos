from enum import Enum

class KVOperatorType(Enum):
    READ = 1
    WRITE = 2
    DELETE = 3
    
class KVStatus(Enum):
    SUCC = 0
    FAIL = -1
    KEY_NOTEXIST = 1
    VERSION_CONFLICT = -11
    VERSION_NOTEXIST = -12
    
    
NULL_VERSION = 0