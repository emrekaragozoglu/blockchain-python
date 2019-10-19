# -*- coding: utf-8 -*-

from blockchain import Blockchain
# from wallet import Wallet
# from transaction import Transaction
from uuid import uuid4
import py2p
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
sock = None
addr = None

# THREADS

class UpdatePeersListThread(object):
    def __init__(self):
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        start = True
        # run forever
        while  True:
            time.sleep(1)
            # reinitializing the peersList
            peersList = []
            # populating the peersList
            for socket in sock.routing_table.values():
                peerAddr = socket.addr[0] + ":" + str(socket.addr[1])
                if not peerAddr in peersList:    
                    peersList.append(peerAddr)
            # assigning peersList array to node's peers
            blockchain.peers = peersList

            # in the start, getting the chains from the network and adopting the longest chain
            if start and addr != "**ip_address**:20000":
                sock.send('hello consensus', addr)
                start = False

class MiningThread(object):
    def __init__(self):
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        # run forever
        while  True:
            time.sleep(10)

            # Receiving a reward for finding the proof
            # The sender is "0" to signify that this Node has mined a new coin

            # Running the proof of work algorithm to get the next proof
            last_block = blockchain.last_block
            proof = blockchain.proof_of_work(last_block)

            # Forge the new Block by adding it to the Chain
            previous_hash = blockchain.hash(last_block)
            block = blockchain.new_block(proof= proof, previous_hash=previous_hash)

            # calling consensus
            sock.send('consensus', blockchain.chain)

class ConsensusThread(object):
    def __init__(self):
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        # run forever
        while True:
            time.sleep(5)

            #  printing the wholeChain
            for block in blockchain.wholeChain:
                print(block['index'], block['previous_hash'])

            # # CONSENSUS: Regular check (in hello messages)
            # # if the number if the recived chains are equal to the number of the peers in the network
            # # call the resolve algorithm because it means that all the chains were received by the node
            if len(blockchain.peer_chains) == len(blockchain.peers):
                if blockchain.resolve_conflicts():
                    print("chain replaced with the longer received chain")
                # clearing the chains array
                blockchain.peer_chains = []
                #storing the chain (adding it to wholeChain)
                blockchain.storeChain()
                # telling other nodes to store their chains too
                # sock.send("store chain")

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

    if packets[1] == "hello consensus":
        senderAddr = packets[2]
        print(senderAddr + " has just been connected.")
        sock.send("whole chain", [senderAddr, blockchain.wholeChain, blockchain.chain])

    # must be called in the node initialization and after the mining 
    elif packets[1] == "consensus":
        blockchain.peer_chains.append(packets[2])
        sock.send('chain', blockchain.chain)

    elif packets[1] == "whole chain":
        senderAddr = packets[2][0]
        if senderAddr == addr:
            blockchain.wholeChain = packets[2][1]
            blockchain.chain = packets[2][2]

    elif packets[1] == "store chain":
        blockchain.storeChain()

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

    # create socket for node
    sock = py2p.MeshSocket('0.0.0.0', 20000)
    # to listen all the coming messages
    sock.register_handler(msgHandler)

    # getting the address of the connected peer
    addr = sock.out_addr[0]+ ':' + str(sock.out_addr[1])

    # if the peer is not the master
    if addr != "**ip_address**:20000":
        # connects itself to the master
        try:
            res = sock.connect('**ip_address**', 20000)
            print("Successfully connected to the master.")
        except:
            print("Master not found.")
            sock.close()
            keepAlive = False

    ut = UpdatePeersListThread()
    # mt = MiningThread()
    # ct = ConsensusThread()

    try:
        # run main forever
        while keepAlive:
            command = input("command: ")

            # HEY
            if command == "hey":
                sock.send('hey', addr)

            # CHAIN
            elif command == "get chain":
                print(blockchain.chain)

            elif command == "diffuse chain":
                sock.send('chain', blockchain.chain)

            # TXS
            elif command == "get txs":
                print(blockchain.unvalidated_transactions)

            elif command == "diffuse txs":
                sock.send('txs', blockchain.unvalidated_transactions)

            # PEERS
            elif command == "get peers":
                print(blockchain.peers)

            elif command == "diffuse peers":
                sock.send('peers', blockchain.peers)

            # NETWORK
            elif command == "get network":
                blockchain.network = blockchain.peers.copy()
                blockchain.network.append(addr)
                print(blockchain.network)

            # MINE
            elif command == "mine":
                # Receiving a reward for finding the proof
                # The sender is "0" to signify that this Node has mined a new coin

                # Running the proof of work algorithm to get the next proof
                last_block = blockchain.last_block
                proof = blockchain.proof_of_work(last_block)

                # Forging the new Block by adding it to the Chain
                previous_hash = blockchain.hash(last_block)
                block = blockchain.new_block(proof=proof, previous_hash=previous_hash)

                # calling consensus
                sock.send('consensus', blockchain.chain)

            # CONSENSUS
            elif command == "consensus":
                sock.send('consensus', blockchain.chain)

            # DISCONNECT
            elif command == "q":
                keepAlive = False
                sock.send('disconnected', addr)
                sock.close()
                continue
            else:
                pass
    except KeyboardInterrupt:
        keepAlive = False
        sock.send('disconnected', addr)
        sock.close()