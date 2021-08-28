from transactionpool import transactionpool
from transaction import transaction
from blockchainutils import BlockchainUtils
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from transaction import transaction
from block import block

class wallet():
    def __init__(self):
        self.keyPair = RSA.generate(2048)

    def fromKey(self, file):
        key = ''
        with open(file, 'r') as keyfile:
            key = RSA.importKey(keyfile.read())
        self.keyPair = key

    def sign(self, data):
        dataHash = BlockchainUtils.hash(data)
        signatureSchemeObject = PKCS1_v1_5.new(self.keyPair)
        signature = signatureSchemeObject.sign(dataHash)
        return signature.hex()

    @staticmethod
    def signatureValid(date, signature, publicKeyString):
        signature = bytes.fromhex(signature)
        dataHash = BlockchainUtils.hash(data)
        publicKey = RSA.importKey(publicKeyString)
        signatureSchemeObject = PKCS1_v1_5.new(publicKey)
        signatureValid = signatureSchemeObject.verify(dataHash, signature)
        return signatureValid

    def publicKeyString(self):
        publicKeyString = self.keyPair.publickey().exportKey('PEM').decode('utf-8')
        return publicKeyString        

    def createTransaction(self, receiver, amount, type):
        transactions = transaction(
            self.publicKeyString(), receiver, amount, type)
        signature = self.sign(transaction.payload())
        transaction.sign(signature)
        return transactions

    def createBlock(self, transactions, lastHash, blockcount):
        block = block(transactions, lastHash,
                        self.publicKeyString(), blockcount)
        signature = self.sign(block.payload())
        block.sign(signature)
        return block