import os
import struct
import time
import random
from sha256 import sha_256

def create_random_data(size):
    return os.urandom(size)

def create_transaction_files():
    transactions = []
    for i in range(4):
        transaction_data = create_random_data(226)
        with open(f'transaction{i + 1}.txt', 'wb') as f:
            f.write(transaction_data)
        transactions.append(transaction_data)
    return transactions

def load_transaction_files(filenames):
    transactions = []
    for filename in filenames:
        with open(filename, 'rb') as f:
            transactions.append(f.read())
    return transactions

def create_random_previous_hash():
    """Создание случайного хеша предыдущего блока."""
    return os.urandom(32)

def load_previous_hash(filename):
    """Загрузка хеша предыдущего блока из файла."""
    with open(filename, 'rb') as f:
        return f.read()

def merkle_root(transactions):
    """Вычисление корня Меркла для списка транзакций."""
    hashes = [bytes.fromhex(sha_256(tx)) for tx in transactions]
    while len(hashes) > 1:
        if len(hashes) % 2 == 1:
            hashes.append(hashes[-1])
        new_hashes = []
        for i in range(0, len(hashes), 2):
            combined = hashes[i] + hashes[i + 1]
            new_hashes.append(bytes.fromhex(sha_256(combined)))
        hashes = new_hashes
    return hashes[0]

def create_block_header(previous_hash, merkle_root):
    """Создание заголовка блока."""
    block_size = struct.pack('<I', 4 + 32 + 32 + 4 + 4)
    timestamp = struct.pack('<I', int(time.time()))
    nonce = 0
    header = block_size + previous_hash + merkle_root + timestamp
    return header, nonce

def find_valid_nonce(header):
    """Поиск nonce, который делает хеш заголовка блока начинающимся с четырех нулей."""
    nonce = 0
    while True:
        nonce_bytes = struct.pack('<I', nonce)
        block_header = header + nonce_bytes
        block_hash = sha_256(block_header)
        if block_hash.startswith('0000'):
            return block_header, nonce, block_hash
        nonce += 1

def save_block(filename, block):
    """Сохранение блока в файл."""
    with open(filename, 'wb') as f:
        f.write(block)

def main():
    
    choice = input("Выберите действие:\n1. Сгенерировать новые файлы с транзакциями\n2. Использовать существующие файлы\nВведите 1 или 2: ")
    if choice == '1':
        transactions = create_transaction_files()
    elif choice == '2':
        filenames = input("Введите названия файлов с транзакциями через пробел: ").split()
        transactions = load_transaction_files(filenames)
    else:
        print("Неправильный выбор")
        return

    # Меню для выбора источника хеша предыдущего блока
    choice = input("Выберите действие:\n1. Сгенерировать новый файл с хешем заголовка предыдущего блока\n2. Использовать существующий файл\nВведите 1 или 2: ")
    if choice == '1':
        previous_hash = create_random_previous_hash()
    elif choice == '2':
        filename = input("Введите название файла с хешем предыдущего блока: ")
        previous_hash = load_previous_hash(filename)
    else:
        print("Неправильный выбор")
        return

   
    root = merkle_root(transactions)

    
    header, initial_nonce = create_block_header(previous_hash, root)

  
    block_header, valid_nonce, block_hash = find_valid_nonce(header)

    
    save_block('block.dat', block_header)

    
    report = f"""
    Merkle Root: {root.hex()}
    Previous Hash: {previous_hash.hex()}
    Initial Nonce: {initial_nonce}
    Valid Nonce: {valid_nonce}
    Block Hash: {block_hash}
    """

    with open('report.txt', 'w') as f:
        f.write(report)

if __name__ == "__main__":
    main()
