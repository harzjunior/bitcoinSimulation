import os
import sys
import mysql.connector

# Add the project root directory to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database_config import DATABASE_CONFIG

def get_connection():
    return mysql.connector.connect(
        host=DATABASE_CONFIG['host'],
        user=DATABASE_CONFIG['user'],
        password=DATABASE_CONFIG['password'],
        database=DATABASE_CONFIG['database']
    )

def create_wallets_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS wallets (
        id INT AUTO_INCREMENT PRIMARY KEY,
        address VARCHAR(255) NOT NULL,
        private_key VARCHAR(255) NOT NULL
    )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def insert_test_data():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO wallets (address, private_key) VALUES 
    ('1DhEis75J4LrimNKtpYJ2mEZf6i3ngWSTn', 'fb484d25a6ec1a69f62d4c5ad47c26590176629f2710c06bee6297a6a8b76655'),
    ('17vm59UDBtevuh87gmSob5XA1xfKVKikrc', 'df84ecc9f12ca07f12b2920f921fa5554e2aa84e43bc6ee920511f7f183c8fa0')
    """)
    conn.commit()
    cursor.close()
    conn.close()

def get_private_key(address):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT private_key FROM wallets WHERE address=%s", (address,))
    result = cursor.fetchone()
    cursor.fetchall()  # Ensure all results are fetched
    cursor.close()
    conn.close()
    if result:
        return result[0]
    return None

# Create the table and insert test data
create_wallets_table()
insert_test_data()

# Test retrieving the private key
alice_address = '1DhEis75J4LrimNKtpYJ2mEZf6i3ngWSTn'
alice_private_key = get_private_key(alice_address)
print(f"Alice's private key: {alice_private_key}")
