import hashlib
import time
import mysql.connector
from tqdm import tqdm

class Block:
    def __init__(self, version, previous_block_hash, merkle_root, timestamp, target, transactions, nonce=0):
        self.version = version
        self.previous_block_hash = previous_block_hash
        self.merkle_root = merkle_root
        self.timestamp = timestamp
        self.target = target
        self.transactions = transactions
        self.nonce = nonce

    def header(self):
        return (str(self.version) + str(self.previous_block_hash) +
                str(self.merkle_root) + str(self.timestamp) +
                str(self.target) + str(self.nonce))

def mine_block(block, target, transaction_pool):
    start_time = time.time()
    block.transactions = transaction_pool
    approximate_max_nonce = 10**7
    progress_bar = tqdm(total=approximate_max_nonce, desc="Mining Block", unit="nonce", mininterval=1.0)
    
    while int(calculate_hash(block), 16) >= int(target, 16):
        block.nonce += 1
        if block.nonce % 1000 == 0:
            progress_bar.update(1000)
    
    progress_bar.n = block.nonce
    progress_bar.refresh()
    progress_bar.close()
    
    end_time = time.time()
    mining_time = end_time - start_time
    return block, mining_time

def calculate_hash(block):
    block_header = block.header()
    transactions_string = ''.join(str(tx) for tx in block.transactions)
    return hashlib.sha256((block_header + transactions_string).encode('utf-8')).hexdigest()

def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="btc_simulation_db"
    )

def create_block_table(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS blocks (id INT AUTO_INCREMENT PRIMARY KEY, version INT, previous_block_hash VARCHAR(255), merkle_root VARCHAR(255), timestamp BIGINT, target VARCHAR(255), nonce INT)")
    connection.commit()

def save_block_to_database(block):
    connection = connect_to_database()
    cursor = connection.cursor()
    sql = "INSERT INTO blocks (version, previous_block_hash, merkle_root, timestamp, target, nonce) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (block.version, block.previous_block_hash, block.merkle_root, block.timestamp, block.target, block.nonce)
    cursor.execute(sql, val)
    connection.commit()
    connection.close()

def create_difficulty_table(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS difficulty (id INT AUTO_INCREMENT PRIMARY KEY, target VARCHAR(255))")
    connection.commit()
    
def load_difficulty():
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT target FROM difficulty ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()
    connection.close()
    if result:
        return result[0]
    else:
        return "0000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"  # Default value

def save_difficulty(target):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO difficulty (target) VALUES (%s)", (target,))
    connection.commit()
    connection.close()

def create_mining_difficulty_table(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS mining_difficulty (id INT AUTO_INCREMENT PRIMARY KEY, user_name VARCHAR(255), difficulty_target VARCHAR(255))")
    connection.commit()
