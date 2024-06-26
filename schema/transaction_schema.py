def create_transaction_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            sender VARCHAR(255),
            recipient VARCHAR(255),
            amount DECIMAL(18, 8),
            timestamp BIGINT,
            status VARCHAR(50) DEFAULT 'pending'
        )
    """)
    connection.commit()
