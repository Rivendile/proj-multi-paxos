import sys
import os.path
import argparse
from kv_grpc_server import PhxKVServicerImpl
import logging
import grpc
from concurrent import futures
import phxkv_pb2_grpc

logger = logging.getLogger(__name__)

this_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(this_dir))
if True:
    import config

parser = argparse.ArgumentParser(description='Paxos-based Distributed KV Store Server')
parser.add_argument('uid', choices=['A', 'B', 'C'], help='UID of the server. Must be A, B, or C')
parser.add_argument('--master', action='store_true',
                    help='If specified, a dedicated master will be used. If one server specifies this flag, all must')
args = parser.parse_args()

oKVServer = PhxKVServicerImpl(args.uid, config.peers, config.state_files[args.uid], args.master)
ret = oKVServer.Init()
if ret != 0:
    logger.error("KV Service init failed")
    sys.exit(ret)
logger.info("KV Service init success..............")

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
phxkv_pb2_grpc.add_PhxKVServicer_to_server(oKVServer, server)
server.add_insecure_port('[::]:{}'.format(config.grpc_ports[args.uid]))
server.start()
logger.info("Server started..............")
