# bitcoinSimulation/block.py
import time

# defines the Block class and its header
class Block:
    def __init__(self, version, previous_block_hash, merkle_root, target, nonce=0):
        self.version = version
        self.previous_block_hash = previous_block_hash
        self.merkle_root = merkle_root
        self.timestamp = int(time.time())
        self.target = target  # Include target attribute
        self.nonce = nonce

    def header(self):
        return f"{self.version}{self.previous_block_hash}{self.merkle_root}{self.timestamp}{self.target}{self.nonce}"
