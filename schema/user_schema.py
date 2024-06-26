def create_user_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            wallet_address VARCHAR(255) NOT NULL,
            balance DECIMAL(18, 8) NOT NULL DEFAULT 0.0
        )
    """)
    connection.commit()
