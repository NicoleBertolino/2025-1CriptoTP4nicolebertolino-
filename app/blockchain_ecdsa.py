import hashlib
import time
import json
from ecdsa import SigningKey, VerifyingKey, SECP256k1  # Biblioteca para ECDSA

# Classe que representa um bloco da blockchain
class Block:
    def __init__(self, index, sender, recipient, value, previous_hash, public_key, signature):
        self.index = index
        self.timestamp = time.time()
        self.sender = sender
        self.recipient = recipient
        self.value = value
        self.previous_hash = previous_hash
        self.nonce = 0
        self.public_key = public_key # Mantemos a chave pública no bloco para verificação
        self.signature = signature
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.sender}{self.recipient}{self.value}{self.previous_hash}{self.nonce}{self.public_key}{self.signature}"
        return hashlib.sha256(block_string.encode()).hexdigest()

# Classe que representa a Blockchain
class Blockchain:
    def __init__(self, difficulty=4):
        self.chain = []
        self.difficulty = difficulty
        self.create_genesis_block()

    def create_genesis_block(self):
        dummy_key = SigningKey.generate(curve=SECP256k1)
        pubkey_hex = dummy_key.get_verifying_key().to_string().hex()
        signature_hex = dummy_key.sign(b"Genesis block").hex()
        genesis_block = Block(0, "Genesis", "Genesis", 0, "0", pubkey_hex, signature_hex)
        self.chain.append(genesis_block)

    def get_last_block(self):
        return self.chain[-1]

    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * self.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    # Adiciona um novo bloco assinado na blockchain
    def add_block(self, sender_name, recipient, value, private_key):
        sender_pubkey = private_key.get_verifying_key()

        message = f"{sender_name}->{recipient}:{value}".encode()
        # Modificado: A mensagem agora inclui o nome do remetente
        print(f"Mensagem: Transferir {value} moedas de {sender_name} para {recipient}")
        print("------------------------------------------------------------------------------------------------------------------------------\n")

        signature = private_key.sign(message)

        last_block = self.get_last_block()
        new_block = Block(index=last_block.index + 1,
                          sender=sender_name,
                          recipient=recipient,
                          value=value,
                          previous_hash=last_block.hash,
                          public_key=sender_pubkey.to_string().hex(), # Chave pública ainda é armazenada
                          signature=signature.hex())
        new_block.hash = self.proof_of_work(new_block)
        self.chain.append(new_block)
        return new_block # Retorna o bloco para que possamos salvá-lo em JSON

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # Verifica se o hash armazenado corresponde ao hash calculado
            if current.hash != current.compute_hash():
                print(f"Erro: Hash do bloco {current.index} inválido!")
                return False
            # Verifica se o hash anterior corresponde
            if current.previous_hash != previous.hash:
                print(f"Erro: Hash anterior do bloco {current.index} não corresponde ao hash do bloco {previous.index}.")
                return False

            # Modificado: A mensagem para verificação também deve usar o nome do remetente
            message = f"{current.sender}->{current.recipient}:{current.value}".encode()
            pubkey_bytes = bytes.fromhex(current.public_key)
            signature_bytes = bytes.fromhex(current.signature)
            try:
                vk = VerifyingKey.from_string(pubkey_bytes, curve=SECP256k1)
                if not vk.verify(signature_bytes, message):
                    print(f"Erro: Assinatura do bloco {current.index} inválida para a transação: {message.decode()}")
                    return False
            except Exception as e:
                print(f"Erro inesperado durante a verificação da assinatura do bloco {current.index}: {e}")
                return False
        return True

# --- FUNÇÃO PARA SALVAR TRANSAÇÃO EM JSON ---
def save_transaction_to_json(transaction_block, filename="transaction.json"):
    """
    Salva um objeto Block (que representa uma transação assinada) em um arquivo JSON.

    Args:
        transaction_block (Block): O objeto Block a ser salvo.
        filename (str): O nome do arquivo JSON onde a transação será salva.
    """
    # Converter o objeto Block para um dicionário serializável em JSON
    transaction_data = {
        "index": transaction_block.index,
        "timestamp": transaction_block.timestamp,
        "sender": transaction_block.sender,
        "recipient": transaction_block.recipient,
        "value": transaction_block.value,
        "previous_hash": transaction_block.previous_hash,
        "nonce": transaction_block.nonce,
        "public_key": transaction_block.public_key,
        "signature": transaction_block.signature,
        "hash": transaction_block.hash
    }
    with open(filename, 'w') as f:
        json.dump(transaction_data, f, indent=4)
    print(f"Transação salva em '{filename}'")

# Testes e Simulação
if __name__ == "__main__":
    blockchain = Blockchain()

    # Gerar chaves privadas para Alice, Bob e Charlie
    alice_key = SigningKey.generate(curve=SECP256k1)
    bob_key = SigningKey.generate(curve=SECP256k1)
    charlie_key = SigningKey.generate(curve=SECP256k1) # Nova chave para Charlie

    print("\nChaves dos Usuários:")
    print(f"Alice - Privada: {alice_key.to_string().hex()}")
    print(f"Alice - Pública: {alice_key.get_verifying_key().to_string().hex()}")
    print("------------------------------------------------------------------------------------------------------------------------------\n")
    print(f"Bob   - Privada: {bob_key.to_string().hex()}")
    print(f"Bob   - Pública: {bob_key.get_verifying_key().to_string().hex()}")
    print("------------------------------------------------------------------------------------------------------------------------------\n")
    print(f"Charlie - Privada: {charlie_key.to_string().hex()}")
    print(f"Charlie - Pública: {charlie_key.get_verifying_key().to_string().hex()}")
    print("------------------------------------------------------------------------------------------------------------------------------\n")

    print("\n--- Simulando Transações ---")

    # Transação 1: Alice para Bob
    print("\nAdicionando Transação: Alice para Bob (100 moedas)")
    tx1_block = blockchain.add_block("Alice", "Bob", 100, alice_key)
    save_transaction_to_json(tx1_block, "tx_alice_bob.json")

    # Transação 2: Bob para Charlie
    print("\nAdicionando Transação: Bob para Charlie (50 moedas)")
    tx2_block = blockchain.add_block("Bob", "Charlie", 50, bob_key)
    save_transaction_to_json(tx2_block, "tx_bob_charlie.json")

    # Transação 3: Charlie para Alice
    print("\nAdicionando Transação: Charlie para Alice (25 moedas)")
    tx3_block = blockchain.add_block("Charlie", "Alice", 25, charlie_key)
    save_transaction_to_json(tx3_block, "tx_charlie_alice.json")

    # Transação 4: Alice para Charlie
    print("\nAdicionando Transação: Alice para Charlie (75 moedas)")
    tx4_block = blockchain.add_block("Alice", "Charlie", 75, alice_key)
    save_transaction_to_json(tx4_block, "tx_alice_charlie.json")

    print("\n--- Blocos na Blockchain ---")
    for block in blockchain.chain:
        print(f"Bloco {block.index} | Hash: {block.hash}\n  De: {block.sender}\n  Para: {block.recipient}\n  Valor: {block.value}\n  Assinatura: {block.signature[:20]}...\n")

    print("\n--- Verificando todas as transações na Blockchain ---")
    is_valid = blockchain.is_chain_valid()
    print(f"Blockchain válida? {is_valid}")

    if not is_valid:
        print("Atenção: A blockchain contém transações inválidas!")
    else:
        print("Todas as transações na blockchain são válidas.")