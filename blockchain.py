import hashlib
import datetime

class Block:
    def __init__(self, data, previous_hash=''):
        self.timestamp = str(datetime.datetime.now())
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        return hashlib.sha256(
            (self.timestamp + self.data + self.previous_hash).encode()
        ).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block("Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        new_block = Block(data, self.get_latest_block().hash)
        self.chain.append(new_block)

# ✅ VERY IMPORTANT LINE
organ_chain = Blockchain()