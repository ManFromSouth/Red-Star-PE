from blockparser import BlockParser
from encrypt import Encryptor


class File_operator():

    def __init__(self, file_name):
        # имя файла
        self.file_name = file_name
        # данные в файле
        self.__parser = BlockParser()

    def load_file_into_memory(self):
        with open(self.file_name, 'r') as f:
            operational_data = f.readlines()
        for line in operational_data:
            self.__parser.parse_line(line)

    def load_data_into_file(self):
        dp_line = self.__parser.deparse_line()
        with open(self.file_name, 'w') as f:
            while dp_line is not None:
                f.write(dp_line)
                dp_line = self.__parser.deparse_line()
                f.write('\n')

    def add_line_to_memory(self, line):
        self.__parser.parse_line(line)

    def get_data_from_memory(self):
        return self.__parser.get_result()

    def encrypt_decrypt_data_in_memory(self, key):
        current_encryptor = Encryptor(key)
        data_snapshot = self.__parser.get_result()
        for line_num, line in enumerate(data_snapshot):
            for block_num, block in enumerate(line):
                self.__parser.replace_block(line_num, block_num,
                                            current_encryptor.encrypt_decrypt_block(block))



if __name__ == '__main__':

    file = File_operator('test_file.txt')
    file.add_line_to_memory('this is a test line')
    file.add_line_to_memory('and this too')
    print(file.get_data_from_memory())
    file.load_data_into_file()
    file.load_file_into_memory()
    print(file.get_data_from_memory())
    file.encrypt_decrypt_data_in_memory('Marx')
    print(file.get_data_from_memory())
    file.encrypt_decrypt_data_in_memory('Marx')
    print(file.get_data_from_memory())
