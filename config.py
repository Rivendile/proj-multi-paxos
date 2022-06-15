# (IP,UDP Port Number)
peers = dict(A=("127.0.0.1", 1217), B=("127.0.0.1", 1218), C=("127.0.0.1", 1219))

# State files for crash recovery. Windows users will need to modify
# these.
state_files = dict(A="state/A.json", B="state/B.json", C="state/C.json")

db_paths = dict(A="db/A.db", B="db/B.db", C="db/C.db")

# gRPC service port
grpc_ports = dict(A=50054, B=50055, C=50056)
