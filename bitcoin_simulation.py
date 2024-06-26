import time
import logging
from users.userOne import User
from mining.miner import save_block_to_database, load_difficulty, connect_to_database, save_difficulty, Block, mine_block, calculate_hash
from schema.user_schema import create_user_table
from schema.wallet_schema import create_wallet_table
from schema.mining_schema import create_mined_blocks_table, create_mining_difficulty_table
from schema.block_schema import create_block_table
from schema.transaction_schema import create_transaction_table

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_database():
    """Connect to the database and create necessary tables."""
    try:
        connection = connect_to_database()
        create_block_table(connection)
        create_mining_difficulty_table(connection)
        create_mined_blocks_table(connection)
        create_user_table(connection)
        create_wallet_table(connection)
        create_transaction_table(connection)
        connection.close()
        logging.info("Database setup completed successfully.")
    except Exception as e:
        logging.error(f"Error setting up the database: {e}")

def adjust_difficulty(last_time, current_time, target, adjustment_factor=0.05):
    """Adjust the difficulty target based on mining time."""
    time_taken = current_time - last_time
    if time_taken < 10:
        target = int(target, 16) - int(target, 16) * adjustment_factor
    else:
        target = int(target, 16) + int(target, 16) * adjustment_factor
    return hex(int(target))

def main():
    # Connect to the database and create tables if they don't exist
    setup_database()

    user_one = User("UserOne")
    
    version = 1
    previous_block_hash = "0000000000000000000000000000000000000000000000000000000000000000"
    merkle_root = "4d3e4e5a8fba545b98c8d12fb9e8f948d95b2b6e9b8b43c3b8e9c8d8a3c8d8e9"
    block_reward = 10
    transaction_pool = []  # list of transactions

    # Ensure recipient addresses are different
    transaction_pool = [
        user_one.wallet.create_transaction("recipientAddress1", 5),
        user_one.wallet.create_transaction("recipientAddress2", 2)
    ]

    # Create a new block object
    # Added transaction_pool as the last argument
    block = Block(version, previous_block_hash, merkle_root, int(time.time()), "0x0000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", transaction_pool)  # Set nonce to 0 initially
    
    # Load the difficulty target
    target = load_difficulty()  # Load the difficulty target from wherever you are storing it

    # Mine the block
    # Added transaction_pool as an argument to the mine_block function call
    mined_block, mining_time = mine_block(block, target, transaction_pool)
    
    # Adjust difficulty based on mining time
    new_target = adjust_difficulty(block.timestamp, mined_block.timestamp, target)

    # Save the mined block to the database
    save_block_to_database(mined_block)
    
    # Save the new difficulty
    save_difficulty(new_target)

    # Log the mined block details
    logging.info(f"UserOne mined a block in {mining_time:.2f} seconds")
    logging.info(f"Wallet balance: {user_one.wallet.get_balance():.8f} BTC")
    logging.info(f"Wallet address: {user_one.wallet.get_address()}")
    logging.info(f"Mined Block Details:")
    logging.info(f"Nonce: {mined_block.nonce}")
    logging.info(f"Hash: {calculate_hash(mined_block)}")  # Ensure the hash is logged correctly
    logging.info(f"Timestamp: {mined_block.timestamp}")
    logging.info(f"New Target: {new_target}")

if __name__ == "__main__":
    main()
