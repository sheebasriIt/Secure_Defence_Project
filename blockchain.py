import json
import hashlib
import datetime

CHAIN_FILE = 'logchain.json'

def load_chain():
    try:
        with open(CHAIN_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_chain(chain):
    with open(CHAIN_FILE, 'w') as file:
        json.dump(chain, file, indent=4)

def create_block(action, filename, chain):
    index = len(chain) + 1
    timestamp = datetime.datetime.now().isoformat()
    previous_hash = chain[-1]['hash'] if chain else '0'
    data = {
        'index': index,
        'timestamp': timestamp,
        'action': action,
        'filename': filename,
        'previous_hash': previous_hash
    }
    block_string = json.dumps(data, sort_keys=True).encode()
    block_hash = hashlib.sha256(block_string).hexdigest()
    data['hash'] = block_hash
    return data

def add_block(action, filename):
    chain = load_chain()
    new_block = create_block(action, filename, chain)
    chain.append(new_block)
    save_chain(chain)
def is_chain_valid(chain):
    for i in range(1, len(chain)):
        current = chain[i]
        previous = chain[i - 1]

        prev_data = previous.copy()
        prev_hash = prev_data.pop('hash')
        recalculated_prev_hash = hashlib.sha256(json.dumps(prev_data, sort_keys=True).encode()).hexdigest()

        if current['previous_hash'] != prev_hash:
            return False

        curr_data = current.copy()
        curr_hash = curr_data.pop('hash')
        recalculated_curr_hash = hashlib.sha256(json.dumps(curr_data, sort_keys=True).encode()).hexdigest()

        if curr_hash != recalculated_curr_hash:
            return False
    return True