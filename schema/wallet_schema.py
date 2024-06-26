def create_wallet_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wallet (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_name VARCHAR(255),
            wallet_address VARCHAR(255),
            balance DECIMAL(18, 8)
        )
    """)
    connection.commit()
