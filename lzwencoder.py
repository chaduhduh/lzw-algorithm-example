import copy


class LzwEncoder(object):

    def __init__(self, main_dictionary=None):
        self._main_dictionary = main_dictionary

    def set_main_dictionary(self, main_dictionary):
        self._main_dictionary = main_dictionary

    def get_main_dictionary(self):
        return copy.copy(self._main_dictionary)

    def find_by_symbol(self, dictionary, symbol):
        return next((item for item in dictionary
                     if item['symbol'] == symbol), None)

    def find_by_decimal(self, dictionary, decimal):
        return next((item for item in dictionary
                     if item['decimal'] == decimal), None)

    def find_by_binary(self, dictionary, binary):
        binary = binary or -1
        return next((item for item in dictionary
                    if str(format(item['decimal'], 'b')) == str(int(binary))), None)

    def get_byte_size(self, dictionary):
        return len(format(len(dictionary), 'b'))

    def add_entry(self, dictionary, symbol):
        dictionary.append({
            'symbol': symbol,
            'decimal': len(dictionary),
            'binary': format(len(dictionary), '0{0}b'.format(self.get_byte_size(dictionary) + 1))
        })

    def encode(self, encode_string):
        response = ""
        current = ""
        main_dict = self.get_main_dictionary()

        for read_character in encode_string:
            if self.find_by_symbol(main_dict, current+read_character):
                current += read_character
                continue
            item = self.find_by_symbol(main_dict, current)
            if item:
                response += format(
                    item['decimal'],
                    '0{0}b'.format(self.get_byte_size(main_dict))
                )
            self.add_entry(main_dict, current+read_character)
            # reset the starting char
            current = read_character
        return response

    def decode(self, decode_string):
        response = ""
        ch = ""
        i = 0
        prev_code = None
        main_dict = self.get_main_dictionary()
        added_item = None

        while i < len(decode_string) + 1:
            byte_size = len(format(len(main_dict) + 1, 'b'))
            current_code = decode_string[i:i+byte_size]
            found_item = self.find_by_binary(main_dict, current_code)
            if found_item:
                ch = found_item['symbol'][0:1]
            if prev_code:
                added_item = self.find_by_binary(main_dict, prev_code)
            if added_item:
                response += added_item['symbol']
                self.add_entry(main_dict, added_item['symbol'] + ch)
            prev_code = current_code
            i += byte_size
        return response or ""

    def test_result(self, original, encoded, decoded):
        print("\nOriginal:\n--------------------")
        print("Entry: ", original, "\n")
        print("length: ", str(len(original)*5) + "\n")
        print("Encoded: ", str(encoded), "\n\n")
        print("Decoded - Should Match Original:\n--------------------")
        print("Entry: ", str(encoded), "\n")
        print("Decoded: ", decoded , "\n")
        print("length: ", str(len(encoded)))
        if decoded == original[:-1] and decoded == self.decode(encoded):
            print("\nStatus:  success!")
        else:
            print("\nStatus:  FAIL")
        print("\n\n\n")
