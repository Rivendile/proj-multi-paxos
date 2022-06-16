# (IP,UDP Port Number)
peers = dict(A=("127.0.0.1", 1220), B=("127.0.0.1", 1221), C=("127.0.0.1", 1222))

# State files for crash recovery. Windows users will need to modify
# these.
state_files = dict(A="state/A.json", B="state/B.json", C="state/C.json")

db_paths = dict(A="db/A.db", B="db/B.db", C="db/C.db")

# gRPC service port
grpc_ports = dict(A=50051, B=50052, C=50053)
