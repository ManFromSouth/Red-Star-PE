import hashlib as hl


class Encryptor:
    """
        Организация работы блочного шифрования. Применяется алгоритм вида ECB
    """
    def __init__(self, key, encoding='utf-8'):
        # Размер блока в байтах
        self.__block_size = 8
        hash_obj = hl.sha256()
        byte_key = bytes(key, encoding)
        hash_obj.update(byte_key)
        self.__hash_key = hash_obj.digest()
        self.__key_pointer = 0

    def encrypt_decrypt_block(self, block):
        result = bytearray([bl_char ^ key_char for (bl_char, key_char) in
                            zip(block, self.__hash_key[self.__key_pointer:self.__key_pointer+8])])
        # хэш sha256 состоит из 32 байтов
        self.__key_pointer += self.__block_size
        if self.__key_pointer >= 32:
            self.__key_pointer = 0
        return result

    def drop_key_pointer(self):
        # устанавливает указатель хэш-ключа на 0
        self.__key_pointer = 0

    def calculate_key_pointer(self, blocks):
        # расчитывает положение указателя хэш-ключа в зависимости от количества пройденых блоков
        _, mod = divmod(blocks*self.__block_size, 32)
        self.__key_pointer = mod


if __name__ == '__main__':
    e_test = Encryptor('test')
    test_block = e_test.encrypt_decrypt_block(b'testtest')
    print(test_block)
    e_test.drop_key_pointer()
    test_block2 = e_test.encrypt_decrypt_block(test_block)
    print(test_block2)
