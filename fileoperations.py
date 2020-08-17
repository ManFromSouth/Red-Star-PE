from blockparser import BlockParser
from encrypt import Encryptor


class File_operator():

    def __init__(self, file_name):
        # имя файла
        self.file_name = file_name
        # данные в файле
        self.__parser = BlockParser()

    def load_encrypted_file_into_memory(self, key = None):
        with open(self.file_name, 'rb') as f:
            operational_data = bytearray(f.read())
        if key is not None:
            current_encryptor = Encryptor(key)
            for pointer in range(int(len(operational_data)/8)):
                operational_data[pointer*8:pointer*8+8] = current_encryptor.encrypt_decrypt_block(
                    operational_data[pointer*8:pointer*8+8])
        self.__parser.load_array(operational_data)


    def load_data_into_file(self):
        result = self.__parser.get_result()
        with open(self.file_name, 'wb') as f:
            for line in result:
                for block in line:
                    f.write((block))

        '''
        try:
            dp_line = self.__parser.rebuild_line().encode('utf-8')
            with open(self.file_name, 'wb') as f:
                while dp_line > b'':
                    f.write(dp_line)
                    dp_line = self.__parser.rebuild_line().encode('utf-8')
        except AttributeError:
            pass'''

    def add_line_to_memory(self, line):
        self.__parser.parse_line(line)

    def get_data_from_memory(self):
        return self.__parser.get_result()

    def encrypt_decrypt_data_in_memory(self, key):
        current_encryptor = Encryptor(key)
        current_encryptor.drop_key_pointer()
        data_snapshot = self.__parser.get_result()
        for line_num, line in enumerate(data_snapshot):
            for block_num, block in enumerate(line):
                self.__parser.replace_block(line_num, block_num,
                                            current_encryptor.encrypt_decrypt_block(block))



if __name__ == '__main__':

    file = File_operator('test_file.txt')
    file.add_line_to_memory('this is a test line')
    file.add_line_to_memory('and this too')
    file.add_line_to_memory('а это на Русском')
    print(file.get_data_from_memory())
    file.encrypt_decrypt_data_in_memory('Marx')
    file.load_data_into_file()
    file.load_encrypted_file_into_memory('Marx')
    # file.encrypt_decrypt_data_in_memory('Marx')
    print(file.get_data_from_memory())