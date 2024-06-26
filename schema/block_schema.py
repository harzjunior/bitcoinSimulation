def create_block_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS blocks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            version INT,
            previous_block_hash VARCHAR(255),
            merkle_root VARCHAR(255),
            timestamp BIGINT,
            target VARCHAR(255),
            nonce INT
        )
    """)
    connection.commit()
