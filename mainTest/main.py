import sys
import os
import ecdsa

# Add the project root directory to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.transaction import Transaction

if __name__ == "__main__":
    sender_private_key = 'fb484d25a6ec1a69f62d4c5ad47c26590176629f2710c06bee6297a6a8b76655'
    recipient_address = '17vm59UDBtevuh87gmSob5XA1xfKVKikrc'
    amount = 15.0
    fee = 0.01

    # Derive public key from private key
    signing_key = ecdsa.SigningKey.from_string(bytes.fromhex(sender_private_key), curve=ecdsa.SECP256k1)
    verifying_key = signing_key.verifying_key
    sender_public_key = verifying_key.to_string().hex()

    # Create transaction
    transaction = Transaction(sender_public_key, sender_private_key, recipient_address, amount, fee)
    transaction.add_input('00000000', 0)
    transaction.add_output(recipient_address, amount)

    # Sign transaction
    transaction.sign_transaction()
    print(f"Transaction signature: {transaction.inputs[0]['signature']}")

    # Verify transaction
    verified = transaction.verify_transaction()
    print(f"Transaction verified: {verified}")