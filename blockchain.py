# -*- coding: utf-8 -*-

# blockchain.py

import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4
from argparse import ArgumentParser

class Blockchain(object):
    # Difficuly of Proof-Of-Work algorithm
    difficulty = 4

    def __init__(self):
        self.wholeChain = [] # full chain
        self.chain = [] # an initial empty list (to store temporary and shorter chain)
        self.unvalidated_transactions = [] # a list to store the unvalidated transactions
        self.peer_chains = [] # a temporary list to store peer chains
        self.peers = [] # peers of the node
        self.network = [] # the whole network that the node belongs to

        # Creating the genesis block
        self.new_block(previous_hash=1, proof=100)
        
    def new_block(self, proof, previous_hash=None):
        # Creates a new Block and adds it to the chain
        ''' proof: proof given by the proog of work algo
            previous_hash: has of the previous block
            returns a new block (which is a dictionary)
        '''
        block = {
            'index': len(self.wholeChain) + 1, # index of the new block = index of the last block + 1
            'timestamp': time(),
            'transactions': self.unvalidated_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]) # hash of the previous chain
        }

        # Resetting the unvalidated list of transactions
        self.unvalidated_transactions = []

        # Appending the block to the chain
        self.chain.append(block)

        return block
        
    def add_new_unvalidated_transaction(self, tx):
        # Adds a new transaction to the list of transactions
        '''
            senderWallet: Wallet of the sender
            recipientWalletWallet: Wallet of the recipient
            amount: amount
            returns the index of the block that will hold this transaction!
        '''
        self.unvalidated_transactions.append(tx)

        return self.last_block['index'] + 1
    
    @staticmethod
    def hash(block):
        # Hashes a Block
        '''
            creates a SHA-256 hash of a block
            returns string (a hash)
        '''
        # we must make sure that dictionary is ordered, otherwise we could have inconsistent hashes
        # converting into a json object by preserving the order and encoding it into a string
        block_string = json.dumps(block, sort_keys = True).encode() 

        return hashlib.sha256(block_string).hexdigest() # creating a hash fromthe encoded string

    @property
    def last_block(self):
        # Returns the last Block in the chain
        return self.chain[-1]

    def proof_of_work(self,last_block):
        '''
            Simple proof of work algorithm:
            - Find a number p' such that hash(pp') contains 4 leading zeroes
            - p: previous proof
            - p': new proof

            returns the proof (int)
        '''
        last_proof = last_block['proof']
        last_hash = self.hash(last_block)

        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1

        return proof
        
    @staticmethod
    def valid_proof(last_proof,proof,last_hash):
        '''
            Validates the Proof: Does hash(last_proof,proof) contains 4 leading zeroes?
            
            returns True or False
        '''
        s = str(last_proof) + str(proof) + str(last_hash)
        guess = s.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        # return True is the first 4 characters of the generated hash is "0000"
        return guess_hash[:4] == "0" * Blockchain.difficulty 

    def register_node(self, address):
        '''
            Addding a new Node to the list of peers
            address: address of the node such as http://localhost:5001

            returns nothing
        '''
        parsed_url = urlparse(address)
        self.peers.add(parsed_url.netloc) # self represents the blockchain object here

    def valid_chain(self, chain):
        '''
            Making sure that the given chain is valid by controling block by block
            Checking if a chain is valid by looping through each block and verifying both 
            the hash and the proof.

            chain: is the blockchain itself (is a list object)
    
            returns boolean (True if the chain is valid, otherwise False)
        '''
        # Starting the check from the beginning (the first block - Genesis block)
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]

            # Checking that the hash value is correct
            # block is the one that is one ahead from the last_block
            last_block_hash = self.hash(last_block)
            if block['previous_hash'] != last_block_hash:
                return False

            # Checking that the Proof Of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof'], last_block_hash):
                return False

            # Advancing the block
            last_block = block
            current_index += 1

        return True 

    def resolve_conflicts(self):
        '''
            Consensus algorithm
            Making sure that the each Node has the longest chain
            returns True if the chain was replaced, False if not

            We can ensure that the longest chain will be the dominant one,
            and will be used as a de-facto chain after the consensus
        '''
        # We only look the chains longer than ours
        selfChain = self.chain.copy()
        self_chain_length = len(selfChain) # the length of our chain itself

        # Getting all the chains from all the peers in our network
        for peer_chain in self.peer_chains:

            peer_chain_length = len(peer_chain) # getting the length of the pper chain
            peer_chain_chain = peer_chain # getting the chain itself

            # Checking if the length is longer and the chain is valid
            if peer_chain_length > self_chain_length and self.valid_chain(peer_chain_chain):
                # assigning the new longer length as a max length
                self_chain_length = peer_chain_length
                # assigning this longer chain as a new_chain
                # self.chain = peer_chain_chain 
                self.chain = peer_chain_chain 

        # return true if replaced
        if selfChain == self.chain:
            return False
        else:
            return True


    def storeChain(self):
        # with open('chain.txt', 'w') as f:
        #     for item in self.chain:
        #         f.write("%s\n" % item)
        for block in self.chain[:-1]:
            self.wholeChain.append(block)

        self.chain = self.chain[len(self.chain)-1:]
