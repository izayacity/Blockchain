# Responsible for managing the chain.
# It will store transactions and have some helper methods for adding new blocks to the chain.
# Here is an example of what a single Block looks like:
#
# block = {
#     'index': 1,
#     'timestamp': 1506057125.900785,
#     'transactions': [
#         {
#             'sender': "8527147fe1f5426f9dd545de4b27ee00",
#             'recipient': "a77f5cdfa2934df3954a5c7c7da5df1f",
#             'amount': 5,
#         }
#     ],
#     'proof': 324984774000,
#     'previous_hash': "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
# }
import hashlib
import json
import requests
from time import time
from urllib.parse import urlparse

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()
        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

    # Create a new block and add it to the chain
    # proof: <int> The proof given by the Proof of Work algorithm
    # previous_hash: <str> Hash of previous Block
    # return: <dict> New Block
    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }
        # Reset the current list of transactions
        self.current_transactions = []
        self.chain.append(block)
        return block

    # Add a new transaction to the list of transactions.
    # Creates a new transaction to go into the next mined block.
    # sender: <str> Address of the sender.
    # recipient: <str> Address of the recipient.
    # amount: <int> Amount.
    # return: <int> The index of the block which the transaction will be added to - the next one to be mined.
    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })
        return self.last_block['index'] + 1

    # Hash a block
    # We must make sure that the dict is ordered, or we'll have inconsistent hashes
    # Creates a SHA-256 hash of a Block
    # block: <dict> Block
    # return: <str>
    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    # Return the last block in the chain
    @property
    def last_block(self):
        return self.chain[-1]

    # Simple Proof of Work Algorithm:
    # - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'.
    # - p is the previous proof, and p' is the new proof.
    # last_proof: <int>
    # return: <int>
    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    # Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
    # last_proof: <int> Previous Proof
    # proof: <int> Current Proof
    # return: <bool> True if correct, False if not.
    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    # Add a new node to the list of nodes
    # address: <str>    Address of node. Eg, 'http://192.168.0.5:5000'
    # return: None
    def register_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    # Determine if a given blockchain is valid
    # chain: <list> A blockchain
    # return: <bool> True if valid, False if not
    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]

            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # Check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True

    # A conflict is when one node has a different chain to another node.
    # Consensus Algorithm: it resolves conflicts by replacing our chain with the longest one in the network.
    # return: <bool> True if our chain was replaced, False if not.
    def resolve_conflicts(self):
        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False
