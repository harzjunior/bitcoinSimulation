def create_mined_blocks_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mined_blocks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_name VARCHAR(255),
            nonce BIGINT,
            hash VARCHAR(255),
            timestamp BIGINT,
            mining_time DOUBLE,
            difficulty_target VARCHAR(255),
            wallet_address VARCHAR(255)
        )
    """)
    connection.commit()