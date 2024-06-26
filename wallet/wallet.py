# bitcoinSimulationCopied/wallet.py
import time
import ecdsa
import hashlib
import base58
import mysql.connector

class Wallet:
    def __init__(self, user_name):
        self.user_name = user_name
        self.address = self.load_or_create_address()
        self.balance = self.load_balance()
        self.private_key = self.load_or_generate_private_key()  # Load or generate private key
        print(f"Initialized Wallet with address: {self.address}")
        
        # Generate a new private key if not loaded from database
        self.private_key = self.load_or_generate_private_key()

    def generate_address(self):
        private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        public_key = private_key.get_verifying_key().to_string()
        sha256_1 = hashlib.sha256(public_key).digest()
        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(sha256_1)
        hashed_public_key = ripemd160.digest()
        versioned_payload = b'\x00' + hashed_public_key
        sha256_2 = hashlib.sha256(versioned_payload).digest()
        sha256_3 = hashlib.sha256(sha256_2).digest()
        checksum = sha256_3[:4]
        binary_address = versioned_payload + checksum
        return base58.b58encode(binary_address).decode('utf-8')

    def add_reward(self, reward):
        self.balance += reward
        self.save_balance()

    def get_balance(self):
        return self.balance

    def get_address(self):
        return self.address

    def save_balance(self):
        connection = self.connect_to_database()
        cursor = connection.cursor()
        sql = "UPDATE users SET balance = %s WHERE wallet_address = %s"
        cursor.execute(sql, (self.balance, self.address))
        connection.commit()
        connection.close()

    def load_balance(self):
        connection = self.connect_to_database()
        cursor = connection.cursor()
        sql = "SELECT balance FROM users WHERE wallet_address = %s"
        cursor.execute(sql, (self.address,))
        result = cursor.fetchone()
        connection.close()
        if result:
            return result[0]
        return 0.0

    def load_or_create_address(self):
        connection = self.connect_to_database()
        cursor = connection.cursor()
        sql = "SELECT wallet_address FROM users WHERE username = %s"
        cursor.execute(sql, (self.user_name,))
        result = cursor.fetchone()
        if result:
            connection.close()
            return result[0]
        else:
            new_address = self.generate_address()
            self.balance = 0.0  # Initialize balance for the new user
            sql = "INSERT INTO users (username, wallet_address, balance) VALUES (%s, %s, %s)"
            cursor.execute(sql, (self.user_name, new_address, self.balance))
            connection.commit()
            connection.close()
            return new_address

    def load_or_generate_private_key(self):
        # Load or generate a new private key securely
        connection = self.connect_to_database()
        cursor = connection.cursor()
        sql = "SELECT private_key FROM users WHERE wallet_address = %s"
        cursor.execute(sql, (self.address,))
        result = cursor.fetchone()
        connection.close()

        if result and result[0]:
            private_key = result[0]
        else:
            # Generate a new private key if not already stored
            private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1).to_string().hex()
            # Store the private key in the database for future use
            connection = self.connect_to_database()
            cursor = connection.cursor()
            sql = "UPDATE users SET private_key = %s WHERE wallet_address = %s"
            cursor.execute(sql, (private_key, self.address))
            connection.commit()
            connection.close()

        return private_key

    def connect_to_database(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="btc_simulation_db"
        )
    
    def sign_transaction(self, transaction_data):
        # Use the private key to sign the transaction_data
        signing_key = ecdsa.SigningKey.from_string(bytes.fromhex(self.private_key), curve=ecdsa.SECP256k1)
        signature = signing_key.sign(str(transaction_data).encode())
        return base58.b58encode(signature).decode('utf-8')

    def create_transaction(self, recipient_address, amount):
        if self.balance < amount:
            raise ValueError("Insufficient balance for the transaction")

        transaction = {
            'sender': self.address,
            'recipient': recipient_address,
            'amount': amount,
            'timestamp': int(time.time()),
            'status': 'pending'
        }
        self.save_transaction(transaction)
        return transaction
    
    def save_transaction(self, transaction):
        connection = self.connect_to_database()
        cursor = connection.cursor()
        sql = "INSERT INTO transactions (sender, recipient, amount, timestamp, status) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (transaction['sender'], transaction['recipient'], transaction['amount'], transaction['timestamp'], transaction['status']))
        connection.commit()
        connection.close()
    
    def process_pending_transactions(self):
        connection = self.connect_to_database()
        cursor = connection.cursor()
        sql = "SELECT * FROM transactions WHERE status = 'pending'"
        cursor.execute(sql)
        transactions = cursor.fetchall()
        for txn in transactions:
            if txn[1] == self.address and self.balance >= txn[3]:
                self.balance -= txn[3]
                self.update_transaction_status(txn[0], 'completed')
                self.save_balance()
            elif txn[2] == self.address:
                self.balance += txn[3]
                self.update_transaction_status(txn[0], 'completed')
                self.save_balance()
        connection.close()
    
    def update_transaction_status(self, txn_id, status):
        connection = self.connect_to_database()
        cursor = connection.cursor()
        sql = "UPDATE transactions SET status = %s WHERE id = %s"
        cursor.execute(sql, (status, txn_id))
        connection.commit()
        connection.close()
