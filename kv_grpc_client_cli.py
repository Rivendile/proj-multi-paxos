import logging
import os
import sys
from kv_grpc_client import PhxKVClient
import grpc
from kv_enum import KVStatus

logger = logging.getLogger(__name__)

this_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(this_dir))
if True:
    import config

uids=config.peers.keys()
grpc_peers = {
    k: (v[0], config.grpc_ports[k]) for k, v in config.peers.items()
}

current_uid = None
current_client = None


def printHelp():
    sys.stdout.write(f"Available commands:\n")
    sys.stdout.write(f"  help                           - print this help message\n")
    sys.stdout.write(f"  q                              - quit\n")
    sys.stdout.write(f"  connect <UID>                  - connect the gRPC server by UID\n")
    sys.stdout.write(f"  disconnect                     - disconnect current gRPC server\n")
    sys.stdout.write(f"  get <key>                      - get the value of the key\n")
    sys.stdout.write(f"  put <key> <value> <version>    - set the value of the key\n")
    sys.stdout.write(f"  delete <key> <version>         - delete the key\n")
    
def printPeers():
    sys.stdout.write(f"Servers: {grpc_peers}\n")


sys.stdout.write("Welcome to the KV Client CLI.\n")
printHelp()

while True:
    try:
        if current_uid is None:
            printPeers()
            sys.stdout.write("Please select a server to connect to by the UID.\n")
        else:
            sys.stdout.write(f"Current UID: {current_uid}\n")
        sys.stdout.write('> ')
        sys.stdout.flush()
        cmd = sys.stdin.readline().strip()
        command = cmd.split()[0]

        if command == 'help':
            printHelp()
            
        elif command == 'q':
            sys.stdout.write("Exit...\n")
            break
        
        elif command == 'connect':
            uid = cmd.split()[1]
            if uid not in uids:
                sys.stdout.write("Invalid UID.\n")
                continue
            if current_uid is not None:
                sys.stdout.write("Disconnecting current server.\n")
                del current_client
                current_uid = None
            sys.stdout.write(f"Connecting to server {uid}.\n")
            current_client = PhxKVClient(grpc.insecure_channel(grpc_peers[uid][0] + ':' + str(grpc_peers[uid][1])))
            current_uid = uid

        elif command == 'disconnect':
            sys.stdout.write("Disconnecting current server.\n")
            del current_client
            current_uid = None

        elif command == 'get':
            key = cmd.split()[1]
            if current_uid is None:
                sys.stdout.write("Please connect to a server.\n")
                continue
            status, bValue, version = current_client.GetLocal(key)
            if status == KVStatus.SUCC:
                sys.stdout.write(f"Value: {bValue.decode('utf-8')}, Version: {version}\n")
            else:
                sys.stdout.write(f"Error: {status}\n")

        elif command == 'put':
            key, value, version = cmd.split()[1:]
            if current_uid is None:
                sys.stdout.write("Please connect to a server.\n")
                continue
            status = current_client.Put(key, value, version)
            if status != KVStatus.SUCC:
                sys.stdout.write(f"Error: {status}\n")
        
        elif command == 'delete':
            key, version = cmd.split()[1:]
            if current_uid is None:
                sys.stdout.write("Please connect to a server.\n")
                continue
            status = current_client.Delete(key, version)
            if status != KVStatus.SUCC:
                sys.stdout.write(f"Error: {status}\n") 
        
        else:
            sys.stdout.write("Invalid command.\n")
            printHelp()
             
    except Exception as e:
        sys.stdout.write(f"Error: {e}\n")