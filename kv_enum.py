from enum import IntEnum

class KVOperatorType(IntEnum):
    READ = 1
    WRITE = 2
    DELETE = 3
    
class KVStatus(IntEnum):
    SUCC = 0
    FAIL = -1
    KEY_NOTEXIST = 1

if __name__ == "__main__":
    print(int(KVOperatorType.READ))