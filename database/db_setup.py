# database/db_setup.py

from db_connection import get_connection

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

def create_user_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255) NOT NULL, wallet_address VARCHAR(255) NOT NULL, balance DECIMAL(18, 8) NOT NULL DEFAULT 0.0)")
    conn.commit()
    cursor.close()
    conn.close()
    