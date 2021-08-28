from blockchainutils import BlockchainUtils
from transaction import transaction
from wallet import wallet
from transactionpool import transactionpool
from block import block
from blockchain import blockchain 
import pprint
from accountmodel import accountmodel
from node import node
import sys

if __name__ == '__main__':

    ip = sys.argv[1]
    port = int(sys.argv[2])
    apiPort = int(sys.argv[3])
    keyFile = None
    if len(sys.argv) > 4:
        keyFile = sys.argv[4]

    node = node(ip, port, keyFile) 
    node.startP2P()
    node.startAPI(apiPort)



    