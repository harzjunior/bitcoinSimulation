def create_difficulty_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS difficulty (
            id INT AUTO_INCREMENT PRIMARY KEY,
            target VARCHAR(255)
        )
    """)
    connection.commit()