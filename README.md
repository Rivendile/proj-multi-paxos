# Course Project: Multi-paxos

# 0. Introduction
This repository contains the source code for our course project ("Concept and design of distributed system"). 
We implement the toy paxos and multi-paxos supporting echo and kv.
We refer to the implementation of [multi-paxos](https://github.com/cocagne/multi-paxos-example) for the basic part.


# 1. How to use
## Environment config
### Step 1: conda environment
```
conda env create -f multi-paxos.yaml
```
### Step 2: gRPC
```
python -m grpc_tools.protoc -I ./ --python_out=./ --grpc_python_out=. ./kv.proto
```

## Running
### Basic Multi-paxos
```
# Running the server
# Without master leases:
python server.py A|B|C
# With master leases:
python server.py --master A|B|C

# Running the client
python client.py A|B|C <value>
```
### Echo

### KV


# 2. Content
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
- **Echo and KV**