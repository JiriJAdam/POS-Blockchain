class message():
    def __init__(self, senderConnector, messageType, data):
        self.senderConnector = senderConnector
        self.messageType = messageType
        self.data = data