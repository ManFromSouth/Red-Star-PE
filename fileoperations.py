from blockparser import BlockParser
from encrypt import Encryptor


class FileOperator:

    def __init__(self, file_name):
        # имя файла
        self.file_name = file_name
        # данные в файле
        self.__parser = BlockParser()

    def load_encrypted_file_into_memory(self, key=None):
        """
        Загружает данные из файла в парсер
        если Key - не None, то перед этим происходит дешифровка
        считанных данных по этому ключу
        :param key: Ключ шифрования
        """
        with open(self.file_name, 'rb') as f:
            operational_data = bytearray(f.read())
        if key is not None:
            current_encryptor = Encryptor(key)
            for pointer in range(int(len(operational_data)/8)):
                operational_data[pointer*8:pointer*8+8] = current_encryptor.encrypt_decrypt_block(
                    operational_data[pointer*8:pointer*8+8])
        self.__parser.load_array(operational_data)

    def load_data_into_file(self, key=None):
        """
        Загружает данные из парсера в файл.
        Если key - не None, то данные перед этим шифруются
        :param key:  Ключ шифрования
        """
        if key is not None:
            self.__encrypt_decrypt_data_in_memory(key)
        result = self.__parser.get_result()
        with open(self.file_name, 'wb') as f:
            for line in result:
                for block in line:
                    f.write(block)

    def add_line_to_memory(self, line):
        """
        Записывает строку в парсер
        :param line:  записываемая строка
        """
        self.__parser.parse_line(line)

    def get_data_from_memory(self):
        """
        Считывает весь массив байтов в парсере
        :return: массив байтов
        """
        return self.__parser.get_result()

    def __encrypt_decrypt_data_in_memory(self, key):
        """
        По ключу зашифровывает данные в парсере
        :param key: Ключ шифрования
        """
        current_encryptor = Encryptor(key)
        current_encryptor.drop_key_pointer()
        data_snapshot = self.__parser.get_result()
        for line_num, line in enumerate(data_snapshot):
            for block_num, block in enumerate(line):
                self.__parser.replace_block(line_num, block_num,
                                            current_encryptor.encrypt_decrypt_block(block))

    def extract_readable_data(self):
        """
        Удаляет все данные из блоков, возвращая их в пригодном для использования виде
        :return: список строк
        """
        result_list = list()
        dp_line = self.__parser.rebuild_line()
        while dp_line is not None:
            result_list.append(dp_line)
            dp_line = self.__parser.rebuild_line()
        return result_list


if __name__ == '__main__':

    file = FileOperator('test_file.txt')
    file.add_line_to_memory('this is a test line')
    file.add_line_to_memory('and this too')
    file.add_line_to_memory('а это на Русском')
    print(file.get_data_from_memory())
    file.load_data_into_file('Marx')
    file.load_encrypted_file_into_memory('Marx')
    # file.encrypt_decrypt_data_in_memory('Marx')
    print(file.get_data_from_memory())
    print(file.extract_readable_data())
