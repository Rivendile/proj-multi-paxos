import logging
import os
import sys
from kv_grpc_client import PhxKVClient
import grpc
from kv_enum import KVStatus
from utils.utils import log_everything

log_everything()
logger = logging.getLogger(__name__)

this_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(this_dir))
if True:
    import config

uids = config.peers.keys()
grpc_peers = {k: (v[0], config.grpc_ports[k]) for k, v in config.peers.items()}

current_uid = None
current_client = None


def printHelp():
    sys.stdout.write(f"\nAvailable commands:\n")
    sys.stdout.write(f"  help                           - print this help message\n")
    sys.stdout.write(f"  q                              - quit\n")
    sys.stdout.write(
        f"  connect <UID>                  - connect the gRPC server by UID\n"
    )
    sys.stdout.write(
        f"  disconnect                     - disconnect current gRPC server\n"
    )
    sys.stdout.write(f"  get <key>                      - get the value of the key\n")
    sys.stdout.write(f"  put <key> <value>              - set the value of the key\n")
    sys.stdout.write(f"  delete <key>                   - delete the key\n")


def printPeers():
    sys.stdout.write(f"\nAvailable Servers:\n")
    for uid, addr in grpc_peers.items():
        sys.stdout.write(f"  {uid}: {addr}\n")


uid = "A"
current_client = PhxKVClient(
    grpc.insecure_channel(grpc_peers[uid][0] + ":" + str(grpc_peers[uid][1]))
)

sys.stdout.write("Welcome to the KV Client CLI.\n")
printHelp()

while True:
    try:
        if current_uid is None:
            printPeers()
            sys.stdout.write(
                "\nPlease select a server via the command `connect <UID>` first.\n"
            )
        else:
            sys.stdout.write(f"Current UID: {current_uid}\n")
        sys.stdout.write("> ")
        sys.stdout.flush()
        cmd = sys.stdin.readline().strip()
        command = cmd.split()[0]

        if command == "help":
            printHelp()

        elif command == "q":
            sys.stdout.write("Exit...\n")
            break

        elif command == "connect":
            uid = cmd.split()[1]
            if uid not in uids:
                sys.stdout.write("Invalid UID.\n")
                continue
            if current_uid is not None:
                sys.stdout.write("Disconnecting current server.\n")
                del current_client
                current_uid = None
            sys.stdout.write(f"Connecting to server {uid}.\n")
            current_client = PhxKVClient(
                grpc.insecure_channel(
                    grpc_peers[uid][0] + ":" + str(grpc_peers[uid][1])
                )
            )
            current_uid = uid

        elif command == "disconnect":
            sys.stdout.write("Disconnecting current server.\n")
            del current_client
            current_uid = None

        elif command == "get":
            key = cmd.split()[1]
            if current_uid is None:
                sys.stdout.write("Please connect to a server.\n")
                continue
            status, bValue = current_client.GetLocal(key)
            sValue = bValue.decode()
            if status == KVStatus.SUCC:
                sys.stdout.write(f"Value: {sValue}\n")
            else:
                sys.stdout.write(f"Error: {status}\n")

        elif command == "put":
            key, value = cmd.split()[1:]
            if current_uid is None:
                sys.stdout.write("Please connect to a server.\n")
                continue
            status = current_client.Put(key, value.encode())
            if status != KVStatus.SUCC:
                sys.stdout.write(f"Error: {status}\n")

        elif command == "delete":
            key = cmd.split()[1]
            if current_uid is None:
                sys.stdout.write("Please connect to a server.\n")
                continue
            status = current_client.Delete(key)
            if status != KVStatus.SUCC:
                sys.stdout.write(f"Error: {status}\n")

        else:
            sys.stdout.write("Invalid command.\n")
            printHelp()

    except Exception as e:
        sys.stdout.write(f"Error: {e}\n")
