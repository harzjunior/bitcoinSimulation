import os
import sys
import ecdsa

# Add the project root directory to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.transaction import Transaction
from database.db_connection import get_connection

def get_private_key(address):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT private_key FROM wallets WHERE address=%s", (address,))
    result = cursor.fetchone()
    cursor.fetchall()  # Ensure all results are fetched
    conn.close()
    if result:
        return result[0] # Assuming private_key is retrieved as a string
    return None

# Initialize wallets
alice_address = "1DhEis75J4LrimNKtpYJ2mEZf6i3ngWSTn"
bob_address = "17vm59UDBtevuh87gmSob5XA1xfKVKikrc"

# Fetch private keys
alice_private_key = get_private_key(alice_address)
bob_private_key = get_private_key(bob_address)

# Debugging: Print retrieved private keys
print(f"Alice's private key-: {alice_private_key}")
print(f"Bob's private key-: {bob_private_key}")

# Check if private keys are retrieved successfully
if not alice_private_key:
    print(f"Private key for {alice_address} not found in the database.")
    sys.exit(1)
if not bob_private_key:
    print(f"Private key for {bob_address} not found in the database.")
    sys.exit(1)

# Derive public key for Alice
alice_signing_key = ecdsa.SigningKey.from_string(bytes.fromhex(alice_private_key), curve=ecdsa.SECP256k1)
alice_verifying_key = alice_signing_key.verifying_key
alice_public_key = alice_verifying_key.to_string().hex()
# print(alice_public_key)

alice_transaction = Transaction(
    # sender_public_key=alice_address,
    sender_public_key=alice_public_key,  # Use derived public key
    sender_private_key=alice_private_key,
    recipient_address=bob_address,
    amount=50.0,
    fee=0.01
)

# Adding input to the transaction
alice_transaction.add_input(transaction_id='00000000', output_index=0)

# Adding output to the transaction
alice_transaction.add_output(recipient_address=bob_address, amount=50.0)

# Signing the transaction
alice_transaction.sign_transaction()

# Verifying the transaction
is_verified = alice_transaction.verify_transaction()

print(f"Transaction verified: {is_verified}")
