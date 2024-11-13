# Proof-of-Work Algorithm

## Описание

Этот проект реализует базовый алгоритм консенсуса, основанный на концепции **Proof-of-Work (PoW)**, с возможностью адаптации под **Proof-of-Stake (PoS)**. Данный код предназначен для создания транзакций, вычисления корня Меркла и формирования заголовка блока. Используется хеш-функция SHA-256 для обеспечения криптографической стойкости.

### Основные функции

- **Работа с транзакциями:**
  - `create_random_data(size)`: Создает случайные данные указанного размера.
  - `create_transaction_files()`: Генерирует файлы транзакций и сохраняет их на диск.
  - `load_transaction_files(filenames)`: Загружает файлы транзакций из списка имен файлов.
  - `create_random_previous_hash()`: Создает случайный хеш для предыдущего блока.

- **Меркл-дерево:**
  - `merkle_root(transactions)`: Вычисляет корень Меркла из списка транзакций.

- **Создание блока:**
  - `create_block_header(previous_hash, merkle_root)`: Формирует заголовок блока, используя хеш предыдущего блока и корень Меркла.

### Зависимости

- Python 3.x
- Модуль `sha256.py`, реализующий хеш-функцию SHA-256

### Пример использования

```python
from algorithm import create_transaction_files, create_random_previous_hash, merkle_root, create_block_header

# Создаем транзакции
transactions = create_transaction_files()

# Загружаем транзакции
previous_hash = create_random_previous_hash()
root = merkle_root(transactions)

# Создаем заголовок блока
header = create_block_header(previous_hash, root)
print("Заголовок блока:", header)
