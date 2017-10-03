class Blockchain(object):
    def _init_(self):
        self.chain = []
        self.current_transactions = []

    # Create a new block and add it to the chain
    def new_block(self):
        pass

    # Add a new transaction to the list of transactions
    def new_transaction(self):
        pass

    # Hash a block
    @staticmethod
    def hash(block):
        pass

    # Return the last block in the chain
    @property
    def last_block(self):
        pass