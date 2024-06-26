# bitcoinSimulation/tests/test_block.py

import unittest
import os
import sys

# Add the project directory to the Python path before importing wallet
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from bitcoinSimulation.block import Block

class TestBlock(unittest.TestCase):

    def test_block_initialization(self):
        version = 1
        previous_block_hash = "0000000000000000000000000000000000000000000000000000000000000000"
        merkle_root = "4d3e4e5a8fba545b98c8d12fb9e8f948d95b2b6e9b8b43c3b8e9c8d8a3c8d8e9"
        target = "0000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
        block = Block(version, previous_block_hash, merkle_root, target)

        self.assertEqual(block.version, version)
        self.assertEqual(block.previous_block_hash, previous_block_hash)
        self.assertEqual(block.merkle_root, merkle_root)
        self.assertEqual(block.target, target)

    def test_block_header(self):
        version = 1
        previous_block_hash = "0000000000000000000000000000000000000000000000000000000000000000"
        merkle_root = "4d3e4e5a8fba545b98c8d12fb9e8f948d95b2b6e9b8b43c3b8e9c8d8a3c8d8e9"
        target = "0000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
        block = Block(version, previous_block_hash, merkle_root, target)

        header = block.header()
        expected_header = f"{version}{previous_block_hash}{merkle_root}{block.timestamp}{target}{block.nonce}"
        self.assertEqual(header, expected_header)


if __name__ == '__main__':
    unittest.main()