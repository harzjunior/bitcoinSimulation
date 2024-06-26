def create_mining_difficulty_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mining_difficulty (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_name VARCHAR(255),
            difficulty_target VARCHAR(255)
        )
    """)
    connection.commit()