# -*- coding: utf-8 -*-

from blockchain import Blockchain
# from wallet import Wallet
# from transaction import Transaction
from uuid import uuid4
import py2p
import socket
import threading
import time
import sys

# PARAMETERS

# Generate a globally unique address for this Node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

# Instantiate P2P variables
peersList = []
sockToNet1 = None
sockToNet2 = None
sock = None
addr = None
addrToNet1 = None
addrToNet2 = None

# THREADS

class UpdatePeersListThread(object):
    def __init__(self, mode):
        self.mode = mode
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        start = True
        # run forever
        while True:
            time.sleep(1)

            # reinitializing the peersList
            peersList = []

            if mode == 'master':
                # populating the peersList
                for socket in sockToNet1.routing_table.values():
                    peerAddr = socket.addr[0] + ":" + str(socket.addr[1])
                    if not peerAddr in peersList:
                        peersList.append(peerAddr)

                for socket in sockToNet2.routing_table.values():
                    peerAddr = socket.addr[0] + ":" + str(socket.addr[1])
                    if not peerAddr in peersList:
                        peersList.append(peerAddr)

                #  assigning peersList array to node's peers
                blockchain.peers = peersList

            if self.mode == 'slave':
                # populating the peersList
                for socket in sock.routing_table.values():
                    peerAddr = socket.addr[0] + ":" + str(socket.addr[1])
                    if not peerAddr in peersList:
                        peersList.append(peerAddr)

                #  assigning peersList array to node's peers
                blockchain.peers = peersList

            if start and self.mode == 'slave':
                # in the start, getting the chains from the network and adopting the longest chain
                sock.send('hello consensus', addr)
                start = False

class MiningThread(object):
    def __init__(self, mode):
        self.mode = mode
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        # run forever
        while True:
            time.sleep(15)
            # Running the proof of work algorithm to get the next proof
            last_block = blockchain.last_block
            proof = blockchain.proof_of_work(last_block)

            # Forge the new Block by adding it to the Chain
            previous_hash = blockchain.hash(last_block)
            block = blockchain.new_block(proof= proof, previous_hash=previous_hash)

            # calling consensus
            if self.mode == 'master':
                # ? !!! CONSENSUS AMONG NETWORKS !!! ?
                sockToNet1.send('hello consensus', addrToNet1)
                sockToNet2.send('hello consensus', addrToNet2)
            else:
                sock.send('hello consensus', addr)
# FUNCTIONS

# Message handler method for P2P messaging
def msgHandler(msg, handler):
    '''
    msg.packets[0] = type
    msg.packets[1] = flag
    msg.packets[2] = msg
    msg.packets[3] = hash code of the sender
    '''
    packets = msg.packets

    # # -----------------------------------------------------------------------------------------
    # # CONSENSUS: Regular check (in hello messages)
    # # if the number if the recived chains are equal to the number of the peers in the network
    # # call the resolve algorithm because it means that all the chains were received by the node
    # if len(blockchain.peer_chains) == len(blockchain.peers):
    #     if blockchain.resolve_conflicts():
    #         print("chain replaced with the longer received chain")
    #         for i in range(0, len(blockchain.chain)):
    #             print(blockchain.chain[i]['index'], blockchain.chain[i]['previous_hash'])
    #     # clearing the chains array
    #     blockchain.peer_chains = []
    # # -----------------------------------------------------------------------------------------

    if packets[1] == "hello consensus":
        senderAddr = packets[2]
        print(senderAddr + " has just been connected.")
        # sock.send("whole chain", [senderAddr, blockchain.wholeChain, blockchain.chain])

    # must be called in the node initialization and after the mining
    elif packets[1] == "consensus":
        blockchain.peer_chains.append(packets[2])
        sock.send('chain', blockchain.chain)

    # if the chain request has received
    elif packets[1] == "chain":
        # received peer chains are added to the chain array to be used for the consensus
        blockchain.peer_chains.append(packets[2])

    elif packets[1] == "txs":
        print(packets[2])

    elif packets[1] == "peers":
        print(packets[2])

    elif packets[1] == "hey":
        print(packets[2] + " has sent you a hey!")

    # If we receive a disconnect message we delete this peer from the list
    elif packets[1] == "disconnected":
        # remove the peer from the list after the disconnect msg has received
        print(packets[2] + " disconnected.")

    else:
        pass

# MAIN
if __name__ == '__main__':
    keepAlive = True

    # mode is either 'master' or 'slave'
    mode = sys.argv[1]

    # if mode is master, in this implementation there are 3 sockets on diff. ports
    if mode == 'master':
        # geting the ports from the args.
        portToNet1 = sys.argv[2]
        portToNet2 = sys.argv[3]

        # for p2p messaging creates sockets on master machine
        sockToNet1 = py2p.MeshSocket('0.0.0.0', int(portToNet1))
        sockToNet2 = py2p.MeshSocket('0.0.0.0', int(portToNet2))

        # to listen all the coming messages from both sockets
        sockToNet1.register_handler(msgHandler)
        sockToNet2.register_handler(msgHandler)

        # getting the address of the connected peer
        addrToNet1 = sockToNet1.out_addr[0] + ':' + str(sockToNet1.out_addr[1])
        addrToNet2 = sockToNet2.out_addr[0] + ':' + str(sockToNet2.out_addr[1])

        # status message
        print("Master is online on ports " + addrToNet1 + " and " + addrToNet1)

    # if mode is slave
    elif mode == 'slave':
        # getting the master ip addresses
        masterIp1 = sys.argv[2]
        masterIp2 = sys.argv[3]

        # getting the network (by port) to connect
        port = sys.argv[4]

        # connects itself to the master on one of the ports of the master,
        sock = py2p.MeshSocket('0.0.0.0', int(port))

        # to listen all the coming messages from both sockets
        sock.register_handler(msgHandler)

        # getting the address of the connected peer
        addr = sock.out_addr[0] + ':' + str(sock.out_addr[1])

        # connecting to the masters
        # to master 1
        try:
            res1 = sock.connect(masterIp1, int(port))
            print("Successfully connected to the master on " + masterIp1)
        except:
            print("Master not found on " + masterIp1)
            sock.close()
            keepAlive = False
        # to master 2
        try:
            res2 = sock.connect(masterIp2, int(port))
            print("Successfully connected to the master on " + masterIp2)
        except:
            print("Master not found on " + masterIp2)
            sock.close()
            keepAlive = False

    else:
        print("You are not providing the correct mode.")

    ht = UpdatePeersListThread(mode)
    # mt = MiningThread(mode)

    if mode == 'master':
        sock = sockToNet1

    try:
        # run main forever
        while keepAlive:
            command = input("command: ")

            # CHAIN
            if command == "get chain":
                print(blockchain.chain)

            elif command == "diffuse chain":
                if mode == 'master':
                    # ? !!! CONSENSUS AMONG NETWORKS !!! ?
                    sockToNet1.send('chain', blockchain.chain)
                    sockToNet2.send('chain', blockchain.chain)
                else:
                    sock.send('chain', blockchain.chain)

            # TXS
            elif command == "get txs":
                print(blockchain.unvalidated_transactions)

            elif command == "diffuse txs":
                if mode == 'master':
                    # ? !!! CONSENSUS AMONG NETWORKS !!! ?
                    sockToNet1.send('txs', blockchain.unvalidated_transactions)
                    sockToNet2.send('txs', blockchain.unvalidated_transactions)
                else:
                    sock.send('txs', blockchain.unvalidated_transactions)

            # PEERS
            elif command == "get peers":
                print(blockchain.peers)

            # NETWORK
            elif command == "get network":
                blockchain.network = blockchain.peers.copy()
                if mode == 'master':
                    blockchain.network.append(addrToNet1)
                    blockchain.network.append(addrToNet2)
                else:
                    blockchain.network.append(addr)

                print(blockchain.network)

            # MINE
            elif command == "mine":
                # Running the proof of work algorithm to get the next proof
                last_block = blockchain.last_block
                proof = blockchain.proof_of_work(last_block)

                # Forging the new Block by adding it to the Chain
                previous_hash = blockchain.hash(last_block)
                block = blockchain.new_block(proof= proof, previous_hash=previous_hash)

                # calling consensus
                # ? !!! CONSENSUS AMONG NETWORKS !!! ?
                if mode == 'master':
                    sockToNet1.send('consensus', blockchain.chain)
                    sockToNet2.send('consensus', blockchain.chain)
                else:
                    sock.send('consensus', blockchain.chain)

            # HEY
            elif command == "hey":
                if mode == 'master':
                    sockToNet1.send('hey', addrToNet1)
                    sockToNet2.send('hey', addrToNet2)
                else:
                    sock.send('hey', addr)

            # DISCONNECT
            elif command == "q":
                keepAlive = False
                if mode == 'master':
                    sockToNet1.send('disconnected', addrToNet1)
                    sockToNet1.close()
                    sockToNet2.send('disconnected', addrToNet2)
                    sockToNet2.close()
                else:
                    sock.send('disconnected', addr)
                    sock.close()
                continue

            else:
                pass
    except KeyboardInterrupt:
        keepAlive = False
        if mode == 'master':
            sockToNet1.send('disconnected', addrToNet1)
            sockToNet1.close()
            sockToNet2.send('disconnected', addrToNet2)
            sockToNet2.close()
        else:
            sock.send('disconnected', addr)
            sock.close()
