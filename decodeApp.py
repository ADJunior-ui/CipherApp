class CipherApp:
    MIN_ASCII = 32
    MAX_ASCII = 126
    MIN_PERSIAN = 1536
    MAX_PERSIAN = 1791

    def __init__(self):
        self.message = ''
        self.key = 0
        self.SepSentenc = []

    def is_valid_text(self, text):
        for ch in text:
            value = ord(ch)
            if not (
                self.MIN_ASCII <= value <= self.MAX_ASCII
                or self.MIN_PERSIAN <= value <= self.MAX_PERSIAN
            ):
                return False
        return True

    def encode_message(self):
        if not self.message:
            self.SepSentenc = []
            return []

        self.SepSentenc = []
        for ch in self.message:
            value = ord(ch) + self.key
            self.SepSentenc.append((value % 10, value // 10))
        return self.SepSentenc

    def decode_message(self):
        decoded = []

        for x, y in self.SepSentenc:
            value = y * 10 + x - self.key
            if 0 <= value <= 0x10FFFF:
                decoded.append(chr(value))
            else:
                decoded.append('?')

        self.message = ''.join(decoded)
        return self.message

    def set_message(self, text):
        self.message = text

    def set_key(self, key):
        self.key = key

    def set_coordinates(self, coordinates):
        self.SepSentenc = coordinates

    def to_coordinate_string(self):
        return ' '.join(f'{x},{y}' for x, y in self.SepSentenc)

    def to_coordinate_list(self):
        return list(self.SepSentenc)

