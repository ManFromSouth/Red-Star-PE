# Разбивает текст на набор блоков

class BlockParser:
    def __init__(self, block_size=8, encoding='utf-8'):
        """
        :param block_size: размер блока в байтах
        :param encoding: кодировка входных/выходных строк. Пока доступна только utf-8
        """
        self.__block_size = block_size
        self.__encoding = encoding
        # результирующие наборы блоков
        self.__result = list()
        # количество добавленных байтов к конечному блоку для каждой строки
        # self.__added_bytes = list()

    def parse_line(self, line):
        """
        преобразует строку в набор блоков размером в block_size байт и добавляет набор в список __result,
        в процессе удаляет из нее последний переход на новую строку
        :param line: преобразуемая строка
        :return:
        """
        # представление строки в байтовом виде
        byte_string = bytearray(line, self.__encoding)
        # размер строки в байтах
        string_size = len(byte_string)
        # количество полных блоков и количество байтов в последнем если он неполный
        blocks_amount, last_bytes = divmod(string_size, self.__block_size)
        sub_line = list()
        for i in range(blocks_amount):
            c_index = i*self.__block_size
            sub_line.append(byte_string[c_index:
                                        c_index+self.__block_size])
        c_index = blocks_amount*self.__block_size
        if last_bytes == 0:
            # если количество остаточных байтов - 0, то вся строка уже была полностью разделена
            leftovers = 0
        else:
            # в противном случае к концу оставшегося блока добавляется необходимое число нулевых байтов
            leftovers = self.__block_size - last_bytes
            last_block = byte_string[c_index:]
            if leftovers > 1:
                for i in range(leftovers-1):
                    last_block += bytearray(b' ')
            last_block += bytearray(b'\n')

            sub_line.append(last_block)
        # все добавляется к свойствам объекта
        self.__result.append(sub_line)
        # self.__added_bytes.append(leftovers)

    def get_result(self):
        return self.__result.copy()

    def get_added_bytes(self):
        return self.__added_bytes.copy()

    def rebuild_line(self):
        """
        достает строчки из аттрибутов __result и __added_bytes по принципу FIFO
        и удаляет их оттуда, преобразуя в читаемый вид
        :return: получаемая строка, если __result - пустой список, то возвращается None
        """
        if len(self.__result) > 0:
            # получение первых элементов списков - аттрибутов
            parsed_string = self.__result[0]
            added_bytes = self.__added_bytes[0]
            # обрубание первых элементов списков - аттрибутов
            self.__result = self.__result[1:]
            # self.__added_bytes = self.__added_bytes[1:]
            # объединение всех блоков в один
            byte_string = bytearray()
            for block in parsed_string:
                byte_string += block
            full_string = byte_string.decode(self.__encoding, 'replace')
            return full_string.rstrip()

        else:
            return None

    # заполняет данные о блоках и добавленных в них байтах
    def load_lines(self, lines_list, bytes_list):
        self.__result = lines_list.copy()
        self.__added_bytes = bytes_list.copy()

    # чистит спсики блоков и добавленных байтов
    def clear_results(self):
        self.__result = list()
        self.__added_bytes = list()

    def replace_block(self, line_num, block_num, block):
        self.__result[line_num][block_num] = block.copy()

    def load_array(self, array):
        self.clear_results()
        string_array = array.decode(self.__encoding, 'ignore').split('\n')
        for line in string_array:
            self.parse_line(line)



if __name__ == '__main__':
    test_object = BlockParser(1, 'utf-16')
    t_line = ''
    test_object.parse_line(t_line)
    print(test_object.rebuild_line())