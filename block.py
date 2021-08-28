import time 
import copy

class block():
    def __init__(self, transactions, lastHash, forger, blockcount):
        self.transactions = transactions
        self.lastHash = lastHash
        self.forger = forger
        self.blockCount = blockcount
        self.timestamp = time.time()
        self.signature = ''

    @staticmethod
    def genesis():
        genesisBlock = block([], 'genesisHash', 'genesis', 0)
        genesisBlock.timestamp = 0
        return genesisBlock

    def toJson(self):
        data = {}
        data['lastHash'] = self.lastHash
        data['forger'] = self.forger
        data['blockcount'] = self.blockCount
        data['timestamp'] = self.timestamp
        data['signature'] = self.signature
        jsonTransactions = []
        for transaction in self.transactions:
            jsonTransactions.append(transaction.toJson())
        data['transactions'] = jsonTransactions
        return data 

    def payload(self):
        jsonRepresentation = copy.deepcopy(self.toJson())
        jsonRepresentation['signature'] = ''
        return jsonRepresentation

    def sign(self, signature):
        self.signature = signature
        
