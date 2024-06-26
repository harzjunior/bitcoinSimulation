# bitcoinSimulation/tests/test_userOne.py

import unittest
import os
import sys

# Add the project directory to the Python path before importing userOne
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from bitcoinSimulation.userOne import User


class TestUser(unittest.TestCase):

    def setUp(self):
        # Remove the mined blocks file, difficulty file, and wallet balance file if they exist
        if os.path.exists('mined_blocks.json'):
            os.remove('mined_blocks.json')
        if os.path.exists('difficulty.json'):
            os.remove('difficulty.json')
        if os.path.exists('wallet_balance.json'):
            os.remove('wallet_balance.json')

    def test_user_initialization(self):
        user = User("TestUser")
        self.assertIsNotNone(user.wallet)
        self.assertEqual(user.difficulty_target, '0000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff')

    def test_mine_block(self):
        user = User("TestUser")
        version = 1
        previous_block_hash = "0000000000000000000000000000000000000000000000000000000000000000"
        merkle_root = "4d3e4e5a8fba545b98c8d12fb9e8f948d95b2b6e9b8b43c3b8e9c8d8a3c8d8e9"
        block_reward = 10

        block, difficulty_target = user.mine(version, previous_block_hash, merkle_root, block_reward)

        self.assertIsNotNone(block)
        self.assertEqual(user.wallet.get_balance(), 10)
        self.assertEqual(difficulty_target, user.difficulty_target)

    def test_difficulty_adjustment(self):
        user = User("TestUser")
        version = 1
        previous_block_hash = "0000000000000000000000000000000000000000000000000000000000000000"
        merkle_root = "4d3e4e5a8fba545b98c8d12fb9e8f948d95b2b6e9b8b43c3b8e9c8d8a3c8d8e9"
        block_reward = 10

        for _ in range(10):
            user.mine(version, previous_block_hash, merkle_root, block_reward)

        # Difficulty should be adjusted
        self.assertNotEqual(user.difficulty_target, '0000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff')

if __name__ == '__main__':
    unittest.main()
