from requests.api import post
from transaction import transaction
from wallet import wallet
from blockchainutils import BlockchainUtils
import requests

def postTransaction(sender, receiver, amount, type):
    transaction = sender.createTransaction(receiver.publicKeyString(), amount, type)
    url = 'http://localhost:5000/transaction'
    package = {'transaction': BlockchainUtils.encode(transaction)}
    request = requests.post(url, json=package)


if __name__ == '__main__':
    bob = wallet()
    alice = wallet()
    alice.fromKey('keys/stakerPrivateKey.pem')
    exchange = wallet()

    # forger: genesis
    postTransaction(exchange, alice, 100, 'EXCHANGE')
    postTransaction(exchange, bob, 100, 'EXCHANGE')
    postTransaction(alice, alice, 25, 'STAKE') 

    # forger: probably alice
    postTransaction(alice, bob, 1, 'TRANSFER')
