# Bitcoin Simulation

This project is a simple simulation of a Bitcoin-like blockchain system. It includes the creation of blocks, mining functionality, wallet management, and difficulty adjustment. The primary goal of this simulation is to provide an educational tool for understanding how Bitcoin mining and blockchain technology work.

1. **Prerequisites**: Specify the versions of Python and any other tools or libraries required.
2. **Detailed Installation Instructions**: Provide detailed steps for setting up the project environment, especially if there are any dependencies or specific settings.
3. **Running Tests**: If there are any tests, include instructions on how to run them.
4. **Configuration Options**: Explain any configuration options or environment variables that can be set.
5. **Examples**: Provide more detailed examples or use cases, if applicable.
6. **Project Background and Motivation**: Briefly explain the motivation or background behind creating this simulation.
7. **Troubleshooting**: Include common issues and troubleshooting steps.
8. **Contribution Guidelines**: Provide guidelines for contributing to the project.
9. **Changelog**: Include a changelog to document changes made over time.

---

## Project Structure

```
bitcoinSimulationCopied/
├── block.py
├── config/
│   └── database_config.py
├── database/
│   └── db_connection.py
├── mainTest/
│   └── main.py
├── main.py
├── miner.py
├── models/
│   ├── __init__.py
│   └── transaction.py
├── tests/
│   ├── __init__.py
│   ├── test_miner.py
│   ├── test_userOne.py
│   └── test_wallet.py
│   └── transaction_test.py
├── transaction.py
├── userOne.py
├── utils/
│   └── crypto_utils.py
├── utils.py
├── wallet.py
└── README.md
```

- `main.py`: The entry point to run the simulation.
- `wallet.py`: Manages the user's wallet, including balance and address generation.
- `utils.py`: Contains utility functions like difficulty conversion.
- `userOne.py`: Represents a user with mining capabilities and manages block mining and difficulty adjustment.
- `miner.py`: Implements the mining logic.
- `block.py`: Defines the `Block` class and its header structure.

## Prerequisites

- Python 3.7 or higher
- `ecdsa` library
- `base58` library
- MySQL server

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/bitcoin-simulation.git
cd bitcoin-simulation
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install dependencies:

```bash
pip install ecdsa base58 mysql-connector-python
```

## Database Configuration

This project uses MySQL to store blockchain data. Before running the simulation, set up a MySQL database and configure the connection in your environment. Update the `db_config.py` file with your database credentials:

```python
# db_config.py

db_config = {
    'host': 'localhost',
    'user': 'username',
    'password': 'password',
    'database': 'bitcoin_simulation'
}
```

## Usage

To run the simulation, execute the `main.py` script:

```bash
python main.py
```

## How It Works

1. **Wallet Initialization**: The `Wallet` class generates a new address and manages the balance. Wallet data is stored in the MySQL database.
  
2. **Mining**: The `User` class in `userOne.py` handles the mining process. It creates a new block with the given parameters and stores mined blocks in the MySQL database.

3. **Difficulty Adjustment**: The difficulty is adjusted every 10 blocks mined by the user. This is a simplified version of the real Bitcoin difficulty adjustment algorithm.

4. **Block Structure**: The `Block` class in `block.py` defines the structure of a block, including its header, version, previous block hash, merkle root, timestamp, target, and nonce.

5. **Mining Logic**: The `miner.py` file contains the `mine_block` function, which iterates over possible nonces to find a valid hash that meets the target.

## Configuration

- Update `db_config.py` with your MySQL database credentials.

## Running Tests

To run the tests for this project, follow these steps:

1. Make sure you have Python 3.7 or higher installed on your system.
2. Navigate to the project directory in your terminal or command prompt.
3. Execute the following command to run all tests:

```bash
python -m unittest discover tests
```

This command will automatically discover and run all test files within the `tests` directory. You should see the test results displayed in your terminal.

## Example Output

After running the simulation, you will see output similar to the following:

```
Initialized Wallet with address: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
UserOne mined a block in 10.24 seconds
Wallet balance: 10 BTC
Wallet address: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
Mined Block Details:
Nonce: 2083236893
Hash: 0000000000000000000000000000000000000000000000000000000000000000
Timestamp: 1617925551
Difficulty adjusted: 0000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff -> 00007fffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
```

## Transaction Class Explanation

The `Transaction` class encapsulates the logic for handling cryptocurrency transactions using ECDSA (Elliptic Curve Digital Signature Algorithm) for signing and verification. Here's a breakdown of its components and functionality:

### Class Structure and Initialization

```python
class Transaction:
    def __init__(self, sender_public_key, sender_private_key, recipient_address, amount, fee):
        self.sender_public_key = sender_public_key
        self.sender_private_key = sender_private_key
        self.recipient_address = recipient_address
        self.amount = amount
        self.inputs = []
        self.outputs = []
        self.fee = fee
```

- **Attributes**: The class initializes with essential attributes such as `sender_public_key`, `sender_private_key`, `recipient_address`, `amount`, `fee`, `inputs`, and `outputs`.
  
- **Inputs and Outputs**: `inputs` and `outputs` are lists that will hold transaction inputs (where the funds are coming from) and outputs (where the funds are going to).

### Methods

#### Adding Inputs and Outputs

```python
    def add_input(self, transaction_id, output_index):
        self.inputs.append({
            'transaction_id': transaction_id,
            'output_index': output_index,
            'signature': ''  # Placeholder for signature
        })

    def add_output(self, recipient_address, amount):
        self.outputs.append({
            'recipient_address': recipient_address,
            'amount': amount
        })
```

- **add_input**: Adds an input to the transaction, typically referencing a previous transaction (`transaction_id`) and its output index (`output_index`).
  
- **add_output**: Adds an output to the transaction, specifying the recipient's address (`recipient_address`) and the amount (`amount`).

#### Signing and Verifying Transactions

```python
    def sign_transaction(self):
        if self.sender_private_key:
            for index, _ in enumerate(self.inputs):
                signature = self.generate_signature()
                self.inputs[index]['signature'] = signature

    def generate_signature(self):
        try:
            signing_key = ecdsa.SigningKey.from_string(
                bytes.fromhex(self.sender_private_key), curve=ecdsa.SECP256k1)
            message = str(self).encode()
            signature = signing_key.sign(message)
            return base58.b58encode(signature).decode('utf-8')
        except Exception as e:
            print(f"Error generating signature: {e}")
            return None

    def verify_transaction(self):
        print(f"Verifying transaction for sender public key: {self.sender_public_key}")

        try:
            verifying_key = ecdsa.VerifyingKey.from_string(
                bytes.fromhex(self.sender_public_key), curve=ecdsa.SECP256k1)
        except ValueError as e:
            print(f"Error: {e}")
            return False

        for input_data in self.inputs:
            if 'signature' not in input_data or not input_data['signature']:
                print("Transaction signature missing.")
                return False
            signature = base58.b58decode(input_data['signature'])
            try:
                verifying_key.verify(signature, str(self).encode())
                print("Signature verified.")
            except ecdsa.BadSignatureError:
                print("Bad signature detected.")
                return False
        return True
```

- **sign_transaction**: Signs the transaction using the sender's private key (`sender_private_key`). It iterates over each input and generates a signature for it.
  
- **generate_signature**: Generates a digital signature for the transaction using ECDSA. It converts the transaction details into a message and signs it using the sender's private key.
  
- **verify_transaction**: Verifies the transaction's signature. It retrieves the sender's public key (`sender_public_key`), reconstructs the message from the transaction details, and verifies the signature against this message.

#### String Representation

```python
    def __str__(self):
        return f"{self.sender_public_key}-{self.recipient_address}-{self.amount}-{self.fee}"
```

- **__str__**: Provides a string representation of the transaction object. This is useful for debugging and logging purposes.

### Example Usage

```python
if __name__ == "__main__":
    sender_private_key = 'fb484d25a6ec1a69f62d4c5ad47c26590176629f2710c06bee6297a6a8b76655'
    recipient_address = '17vm59UDBtevuh87gmSob5XA1xfKVKikrc'
    amount = 5.0
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
```

### Conclusion

This `Transaction` class encapsulates the logic for handling and validating cryptocurrency transactions using ECDSA for digital signatures. It's structured to manage transaction inputs and outputs, sign transactions securely, and verify their authenticity. Integrating this class into a cryptocurrency simulation or application would enable secure and reliable transaction processing.

## Project Background and Motivation

The motivation behind this project is to provide a hands-on understanding of blockchain technology, specifically focusing on Bitcoin's mining process, difficulty adjustment, and wallet management. This simulation serves as an educational tool for developers and enthusiasts interested in exploring blockchain concepts without needing to interact with a real cryptocurrency network.

## Troubleshooting

If you encounter issues, check the following:
- Ensure you are using the correct Python version.
- Verify that all dependencies (`ecdsa`, `base58`, and `mysql-connector-python`) are correctly installed.
- Check database connectivity and ensure MySQL server is running.

## Contribution Guidelines

We welcome contributions! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes.
4. Submit a pull request with a detailed description of your changes.

## Changelog

- **v1.0.0**: Initial release with basic mining and wallet functionalities.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.****