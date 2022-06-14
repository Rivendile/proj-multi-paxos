
# (IP,UDP Port Number)
peers = dict( A=('127.0.0.1',1234),
              B=('127.0.0.1',1235),
              C=('127.0.0.1',1236) )

# State files for crash recovery. Windows users will need to modify
# these.
state_files = dict( A='/home/yihaozhao/multi-paxos-proj/state/A.json',
                    B='/home/yihaozhao/multi-paxos-proj/state/B.json',
                    C='/home/yihaozhao/multi-paxos-proj/state/C.json' )
