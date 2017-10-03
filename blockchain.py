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

class Blockchain(object):
    def _init_(self):
        self.chain = []
        self.current_transactions = []

    # Create a new block and add it to the chain
    def new_block(self):
        pass

    # Add a new transaction to the list of transactions
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
    @staticmethod
    def hash(block):
        pass

    # Return the last block in the chain
    @property
    def last_block(self):
        pass