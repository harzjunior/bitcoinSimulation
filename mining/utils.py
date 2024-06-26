# bitcoinSimulationCopied/utils.py

def target_from_difficulty(difficulty):
    # Convert the difficulty to an integer, then to a hexadecimal string
    return hex(int(difficulty, 16))
