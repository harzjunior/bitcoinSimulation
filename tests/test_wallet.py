# bitcoinSimulation/tests/test_wallet.py

import unittest
import os
import sys

# Add the project directory to the Python path before importing wallet
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from bitcoinSimulation.wallet import Wallet

class TestWallet(unittest.TestCase):

    def setUp(self):
        # Remove the balance file if it exists
        if os.path.exists('wallet_balance.json'):
            os.remove('wallet_balance.json')

    def test_wallet_initialization(self):
        wallet = Wallet()
        self.assertEqual(wallet.get_balance(), 0)
        self.assertIsNotNone(wallet.get_address())

    def test_add_reward(self):
        wallet = Wallet()
        wallet.add_reward(10)
        self.assertEqual(wallet.get_balance(), 10)

    def test_balance_persistence(self):
        wallet = Wallet()
        wallet.add_reward(10)
        wallet.save_balance()

        new_wallet = Wallet()
        self.assertEqual(new_wallet.get_balance(), 10)

    def test_address_persistence(self):
        wallet = Wallet()
        address = wallet.get_address()
        wallet.save_balance()

        new_wallet = Wallet()
        self.assertEqual(new_wallet.get_address(), address)

if __name__ == '__main__':
    unittest.main()
