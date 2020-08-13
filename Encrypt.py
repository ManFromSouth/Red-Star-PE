# Организация работы блочных шифров

class Encryptor:
    def __init__(self):
        # Режим шифрования
        self.encrypt_mode = None
        # Алгоритм шифрования
        self.encrypt_algorithm = None
        # Размер блока в байтах
        self.block_size = 0
