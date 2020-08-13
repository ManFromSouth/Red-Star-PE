"""
    Организация работы блочного шифрования. Применяется алгоритм вида ECB
"""
import hashlib as hl


class Encryptor:
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
        self.__key_pointer += 8
        if self.__key_pointer >= 32:
            self.__key_pointer = 0
        return result

    def drop_key_pointer(self):
        self.__key_pointer = 0


if __name__ == '__main__':
    e_test = Encryptor('test')
    test_block = e_test.encrypt_decrypt_block(b'testtest')
    print(test_block)
    e_test.drop_key_pointer()
    test_block2 = e_test.encrypt_decrypt_block(test_block)
    print(test_block2)
