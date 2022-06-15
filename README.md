# Mult-Paxos
This repository contains the Implementation for the graduate lesson *Concept and design of Distributed System* (2022 Spring, advised by Zhi Yang) in Peking University. We implement the Paxos, the Multi-Paxos Algorithm and a distributed database based on our Paxos consensus protocol.
## Getting Start
- Setup the conda environment.
```bash
conda env create -f multi-paxos.yaml
```
- Autogen the Python code for `grpc` and `protobuf`
```bash
python -m grpc_tools.protoc -I ./ --python_out=./ --grpc_python_out=. ./phxkv.proto
```
If you finish running this command without error, you will see two new files `phxkv_pb2_grpc.py` and `phxkv_pb2.py` in the current directory.
## Usage

### Echo Usage

```bash
# Running the server
# Without master leases:
python server.py A|B|C
# With master leases:
python server.py --master A|B|C

# Running the client
python client.py A|B|C <value>
```

### Paxos-based Distributed Database

- Setup the server A, B and C.
```bash
$ python kv_grpc_server_main.py --help
usage: kv_grpc_server_main.py [-h] [--uid {A,B,C}] [--master]

Paxos-based Distributed KV Store Server

optional arguments:
  -h, --help     show this help message and exit
  --uid {A,B,C}  UID of the server. Must be A, B, or C
  --master       If specified, a dedicated master will be used. If one server
                 specifies this flag, all must         
```
- Interact with the server.
```bash
python kv_grpc_client_cli.py
```

## Content 
- **Basic multi-paxos**
    - **client.py** implements the client.
    - **server.py** implements the server.
    - **config.py** contains required information, such as server IP, port, and path of state files.
    - **messenger.py** contains the message-passing strategy.
    - **composable_paxos.py** contains the core paxos algorithm, including the paxos instance (proposer, accepter, and learner) and related message classes.
    - **replicated_value.py** supports three functions: track and create PaxosInstance, link Messenger and PaxosInstance, and save and restore state.
    - **resolution_strategy.py** ensures that a paxos instance will achieve resolution.
    - **sync_strategy.py** allows a server to send messages to a random peer periodically for synchronization.
    - **master_strategy.py** supports master leases.

## Reference

- [multi-paxos](https://github.com/cocagne/multi-paxos-example): Example multi-paxos application for those learning Paxos & multi-paxos.