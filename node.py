from blockchainutils import BlockchainUtils
from transactionpool import transactionpool
from wallet import wallet
from blockchain import blockchain
from socketCommunication import socketCommunication
from nodeAPI import nodeAPI
from message import message
from blockchainutils import BlockchainUtils
import copy

class node():
    def __init__(self, ip, port, key=None):
        self.p2p = None
        self.ip = ip 
        self.port = port 
        self.transactionpool = transactionpool()
        self.wallet = wallet()
        self.blockchain = blockchain()
        if key is not None:
            self.wallet.fromKey(key)

    def startP2P(self):
        self.p2p = socketCommunication(self.ip, self.port)
        self.p2p.startSocketCommunication(self)
        
    def startAPI(self, apiPort):
        self.api = nodeAPI()
        self.api.injectNode(self)
        self.api.start(apiPort)

    def handleTransaction(self, transaction):
        data = transaction.payload()
        signature = transaction.signature 
        signerPublicKey = transaction.senderPublicKey
        signatureValid = wallet.signatureValid(data, signature, signerPublicKey)
        transactionExists = self.transactionpool.transactionExists(transaction)
        transactionInBlock = self.blockchain.transactionExists(transaction)
        if not transactionExists and not transactionInBlock and signatureValid:
            self.transactionpool.addTransaction(transaction)
            message = message(self.p2p.socketConnector, 'TRANSACTION', transaction)
            encodeMessage = BlockchainUtils.encode(message)
            self.p2p.broadcast(encodeMessage)
            forgingRequired = self.transactionpool.forgerRequired()
            if forgingRequired:
                self.forge()

    def handleBlock(self, block):
        forger = block.forger
        blockHash = block.payload()
        signature = block.signature

        blockCountValid = self.blockchain.blockCountValid(block)
        lastBlockHashValid = self.blockchain.lastBlockHashValid(block)
        forgerValid = self.blockchain.forgerValid(block)
        transactionValid = self.blockchain.transactionValid(block.transactions)
        signatureValid = wallet.signatureValid(blockHash, signature, forger)
        if not blockCountValid:
            self.requestChain()
        if lastBlockHashValid and forgerValid and transactionValid and signatureValid:
            self.blockchain.addBlock(block)
            self.transactionpool.removeFromPool(block.transactions)
            message = message(self.p2p.socketConnector, 'BLOCK', block)
            encodedMessage = BlockchainUtils.encode(message)
            self.p2p.broadcast(encodedMessage)

    def handleBlockchainRequest(self, requestingNode):
        message = message(self.p2p.socketConnector, 'BLOCKCHAIN', self.blockchain)
        encodedMessage = BlockchainUtils.encode(message)
        self.p2p.send(requestingNode, encodedMessage)

    def requestChain(self):
        message = message(self.p2p.socketConnector, 'BLOCKCHAINREQUEST', None)
        encodedMessage = BlockchainUtils.encode(message)
        self.p2p.broadcast(encodedMessage)

    def handleBlockchain(self, blockchain):
        localBlockchainCopy = copy.deepcopy(self.blockchain)
        localBlockCount = len(localBlockchainCopy.blocks)
        receivedChainBlockCount = len(blockchain.blocks)
        if localBlockCount < receivedChainBlockCount:
            for blockNumber, block in enumerate(blockchain.blocks):
                if blockNumber >= localBlockCount:
                    localBlockchainCopy.addBlock(block)
                    self.transactionpool.removeFromPool(block.transactions)
            self.blockchain = localBlockchainCopy

    def forge(self):
        forger = self.blockchain.nextForger()
        if forger == self.wallet.publicKeyString():
            print('I am the next forger')
            block = self.blockchain.createBlock(self.transactionpool.transactions, self.wallet)
            self.transactionpool.removeFromPool(block.transactions)
            message = message(self.p2p.socketConnector, 'BLOCK', block)
            encodedMessage = BlockchainUtils.encode(message)
            self.p2p.broadcast(encodedMessage)
        else:
            print('I am not the next forger')
