import time
import mysql.connector 
import logging
from wallet.wallet import Wallet
from mining.block import Block
from mining.miner import mine_block, connect_to_database, save_block_to_database, load_difficulty, save_difficulty
from mining.utils import target_from_difficulty

class User:
    def __init__(self, name):
        self.name = name
        self.wallet = Wallet(name)
        self.blocks_mined = self.load_mined_blocks_count()
        self.difficulty_target = self.load_difficulty()
        self.min_difficulty_target = '00000000ffffffffffffffffffffffffffffffffffffffffffffffffffffffff'  # Example minimum target
        self.save_wallet_to_database()

    def mine(self, version, previous_block_hash, merkle_root, block_reward, transaction_pool):
        target = target_from_difficulty(self.difficulty_target)
        block = Block(version, previous_block_hash, merkle_root, target)
        block.transactions = transaction_pool
        
        start_time = time.time()
        mined_block, mining_time = mine_block(block, target, transaction_pool)
        end_time = time.time()
        
        self.wallet.process_pending_transactions()
        self.wallet.add_reward(block_reward)
        self.save_wallet_to_database()
        
        block_details = {
            'nonce': mined_block.nonce,
            'hash': mine_block_header_hash(mined_block),
            'timestamp': mined_block.timestamp,
            'mining_time': mining_time,
            'difficulty_target': self.difficulty_target,
            'wallet_address': self.wallet.get_address()
        }
        self.save_mined_block(block_details)
        self.blocks_mined += 1
        
        print(f"{self.name} mined a block in {mining_time:.2f} seconds")
        print(f"Wallet balance: {self.wallet.get_balance()} BTC")
        print(f"Wallet address: {self.wallet.get_address()}")
        print(f"Mined Block Details:")
        print(f"Nonce: {mined_block.nonce}")
        print(f"Hash: {mine_block_header_hash(mined_block)}")
        print(f"Timestamp: {mined_block.timestamp}")
        
        self.difficulty_target = self.adjust_difficulty(self.difficulty_target)
        self.save_difficulty(self.difficulty_target)
        
        return mined_block, self.difficulty_target

    def save_mined_block(self, block_details):
        connection = self.connect_to_database()
        cursor = connection.cursor()
        sql = "INSERT INTO mined_blocks (user_name, nonce, hash, timestamp, mining_time, difficulty_target, wallet_address) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (self.name, block_details['nonce'], block_details['hash'], block_details['timestamp'], block_details['mining_time'], block_details['difficulty_target'], block_details['wallet_address']))
        connection.commit()
        connection.close()

    def load_mined_blocks_count(self):
        connection = self.connect_to_database()
        cursor = connection.cursor()
        sql = "SELECT COUNT(*) FROM mined_blocks WHERE user_name = %s"
        cursor.execute(sql, (self.name,))
        result = cursor.fetchone()
        connection.close()
        if result:
            return result[0]
        return 0

    def adjust_difficulty(self, current_difficulty):
        if self.blocks_mined % 10 == 0:
            new_difficulty = hex(int(current_difficulty, 16) // 2)
            if int(new_difficulty, 16) < int(self.min_difficulty_target, 16):
                new_difficulty = self.min_difficulty_target
            print(f"Difficulty adjusted: {current_difficulty} -> {new_difficulty}")
            return new_difficulty
        return current_difficulty

    def load_difficulty(self):
        return load_difficulty()

    def save_difficulty(self, difficulty_target):
        connection = self.connect_to_database()
        cursor = connection.cursor()
        sql = "INSERT INTO mining_difficulty (user_name, difficulty_target) VALUES (%s, %s) ON DUPLICATE KEY UPDATE difficulty_target = %s"
        cursor.execute(sql, (self.name, difficulty_target, difficulty_target))
        connection.commit()
        connection.close()

    def connect_to_database(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="btc_simulation_db"
        )
    
    def save_wallet_to_database(self):
        connection = self.connect_to_database()
        cursor = connection.cursor()
        sql = "REPLACE INTO wallet (user_name, wallet_address, balance) VALUES (%s, %s, %s)"
        cursor.execute(sql, (self.name, self.wallet.get_address(), self.wallet.get_balance()))
        connection.commit()
        connection.close()

def mine_block_header_hash(block):
    import hashlib
    header = block.header()
    return hashlib.sha256(hashlib.sha256(header.encode('utf-8')).digest()).hexdigest()

def target_from_difficulty(difficulty):
    return hex(int(difficulty, 16))
