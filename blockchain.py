import json
import hashlib
import time
import os

CHAIN_FILE = 'logchain.json'

def load_chain():
    if not os.path.exists(CHAIN_FILE):
        return []
    with open(CHAIN_FILE, 'r') as f:
        return json.load(f)

def save_chain(chain):
    with open(CHAIN_FILE, 'w') as f:
        json.dump(chain, f, indent=4)

def hash_block(block):
    return hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()

def add_block(data):
    chain = load_chain()
    index = len(chain)
    timestamp = time.time()
    previous_hash = hash_block(chain[-1]) if chain else '0'
    block = {
        'index': index,
        'timestamp': timestamp,
        'data': data,
        'previous_hash': previous_hash
    }
    chain.append(block)
    save_chain(chain)

def is_chain_valid(chain):
    for i in range(1, len(chain)):
        if chain[i]['previous_hash'] != hash_block(chain[i-1]):
            return False
    return True