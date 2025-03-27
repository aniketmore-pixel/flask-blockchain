from flask import Flask, jsonify, request, render_template
import time
import hashlib

app = Flask(__name__)

# Blockchain Class Definitions
class Block:
    def __init__(self, index, transactions, previous_hash, nonce=0):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions if isinstance(transactions, list) else [transactions]  # Ensure list
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.find_hash()

    def find_hash(self):
        """Generates SHA-256 hash of the block's contents."""
        block_data = f"{self.index}{self.timestamp}{self.transactions}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_data.encode()).hexdigest()

    def mine_block(self, difficulty):
        """Performs Proof-of-Work to find a valid hash."""
        while self.hash[:difficulty] != "0" * difficulty:
            self.nonce += 1
            self.hash = self.find_hash()

class Blockchain:
    def __init__(self, difficulty=3):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty

    def create_genesis_block(self):
        return Block(0, ["Genesis Block"], "0")  # Ensure transactions is a list

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, transactions):
        transactions = transactions if isinstance(transactions, list) else [transactions]  # Ensure list
        new_block = Block(len(self.chain), transactions, self.get_latest_block().hash)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    @app.route("/validate_chain", methods=["GET"])

    def validate_chain():
        validation_logs = []
    
        for i in range(1, len(aniket_blockchain.chain)):
            current_block = aniket_blockchain.chain[i]
            previous_block = aniket_blockchain.chain[i - 1]

            # Check if stored hash matches recalculated hash
            if current_block.hash != current_block.find_hash():
                log_message = f"⚠️ Block {i} hash mismatch! Stored: {current_block.hash}, Recalculated: {current_block.find_hash()}"
                validation_logs.append(log_message)
                return jsonify({"valid": False, "logs": validation_logs})

            # Check if previous_hash links correctly
            if current_block.previous_hash != previous_block.hash:
                log_message = f"⚠️ Block {i} has wrong previous_hash! Stored: {current_block.previous_hash}, Expected: {previous_block.hash}"
                validation_logs.append(log_message)
                return jsonify({"valid": False, "logs": validation_logs})

        validation_logs.append("✅ Blockchain is valid.")
        return jsonify({"valid": True, "logs": validation_logs})





    def reset_chain(self):
        """Resets the blockchain to its initial state with only the genesis block."""
        self.chain = [self.create_genesis_block()]

# Create a global blockchain instance
aniket_blockchain = Blockchain()

# Home Route
@app.route("/")
def index():
    return render_template("index.html")

# API to View Blockchain
@app.route("/get_chain", methods=["GET"])
def get_chain():
    chain_data = []
    for block in aniket_blockchain.chain:
        chain_data.append({
            "index": block.index,
            "timestamp": block.timestamp,
            "transactions": block.transactions,
            "previous_hash": block.previous_hash,
            "hash": block.hash,
            "nonce": block.nonce
        })
    return jsonify({"chain": chain_data})  # ✅ Return as an object, not a list

# API to Add a New Block
@app.route("/add_block", methods=["POST"])
def add_block():
    data = request.get_json()
    transactions = data.get("transactions", [])
    aniket_blockchain.add_block(transactions)
    return jsonify({"message": "Block added successfully!"})

# API to Validate the Blockchain
@app.route("/validate_chain", methods=["GET"])
def validate_chain():
    is_valid = aniket_blockchain.is_chain_valid()
    return jsonify({"valid": is_valid})

# API to Tamper with Blockchain
@app.route("/tamper_block", methods=["POST"])
def tamper_block():
    data = request.get_json()
    block_index = data.get("index")
    new_transactions = data.get("transactions")

    if 0 < block_index < len(aniket_blockchain.chain):
        aniket_blockchain.chain[block_index].transactions = new_transactions if isinstance(new_transactions, list) else [new_transactions]  # Ensure list
        aniket_blockchain.chain[block_index].hash = aniket_blockchain.chain[block_index].find_hash()
        return jsonify({"message": f"Block {block_index} tampered!"})
    
    return jsonify({"error": "Invalid block index"}), 400

# API to Reset Blockchain
@app.route("/reset_chain", methods=["POST"])
def reset_chain():
    aniket_blockchain.reset_chain()
    return jsonify({"message": "Blockchain reset successfully!"})

if __name__ == "__main__":
    app.run(debug=True)
