import unittest

from decodeApp import CipherApp


class CipherAppTests(unittest.TestCase):
    def setUp(self):
        self.cipher = CipherApp()

    def test_encode_single_ascii_character(self):
        self.cipher.set_message('A')
        self.cipher.set_key(1)
        result = self.cipher.encode_message()
        self.assertEqual(result, [(6, 6)])

    def test_encode_multiple_characters(self):
        self.cipher.set_message('AB')
        self.cipher.set_key(0)
        result = self.cipher.encode_message()
        self.assertEqual(len(result), 2)
        # 'A' = 65, with key 0: (65 % 10, 65 // 10) = (5, 6)
        self.assertEqual(result[0], (5, 6))
        # 'B' = 66, with key 0: (66 % 10, 66 // 10) = (6, 6)
        self.assertEqual(result[1], (6, 6))

    def test_decode_restores_original(self):
        self.cipher.set_coordinates([(6, 6)])
        self.cipher.set_key(1)
        result = self.cipher.decode_message()
        self.assertEqual(result, 'A')

    def test_decode_multiple_coordinates(self):
        self.cipher.set_coordinates([(5, 6), (6, 6)])  # 'A', 'B' with key 0
        self.cipher.set_key(0)
        result = self.cipher.decode_message()
        self.assertEqual(result, 'AB')

    def test_invalid_text_with_newline(self):
        self.assertFalse(self.cipher.is_valid_text('A\nB'))

    def test_invalid_text_with_special_char(self):
        self.assertFalse(self.cipher.is_valid_text('A\x01B'))

    def test_valid_english_text(self):
        self.assertTrue(self.cipher.is_valid_text('Hello World'))

    def test_valid_persian_text(self):
        self.assertTrue(self.cipher.is_valid_text('سلام'))

    def test_valid_mixed_text(self):
        self.assertTrue(self.cipher.is_valid_text('Hello سلام'))

    def test_to_coordinate_string_format(self):
        self.cipher.set_message('A')
        self.cipher.set_key(0)
        self.cipher.encode_message()
        result = self.cipher.to_coordinate_string()
        self.assertEqual(result, '5,6')

    def test_to_coordinate_list_returns_list(self):
        self.cipher.set_coordinates([(1, 2), (3, 4)])
        result = self.cipher.to_coordinate_list()
        self.assertEqual(result, [(1, 2), (3, 4)])

    def test_empty_message_encodes_to_empty_list(self):
        self.cipher.set_message('')
        result = self.cipher.encode_message()
        self.assertEqual(result, [])

    def test_encode_with_large_key(self):
        self.cipher.set_message('A')
        self.cipher.set_key(100)
        result = self.cipher.encode_message()
        value = 65 + 100
        expected = (value % 10, value // 10)
        self.assertEqual(result, [expected])

    def test_decode_with_invalid_unicode(self):
        # Test that decode handles impossible values gracefully
        self.cipher.set_coordinates([(0, 200)])  # 200*10 + 0 = 2000
        self.cipher.set_key(0)
        result = self.cipher.decode_message()
        # Should contain chr or '?' for invalid
        self.assertIsInstance(result, str)

    def test_set_message_updates_message(self):
        self.cipher.set_message('Test')
        self.assertEqual(self.cipher.message, 'Test')

    def test_set_key_updates_key(self):
        self.cipher.set_key(42)
        self.assertEqual(self.cipher.key, 42)

    def test_set_coordinates_updates_coordinates(self):
        coords = [(1, 2), (3, 4)]
        self.cipher.set_coordinates(coords)
        self.assertEqual(self.cipher.SepSentenc, coords)


if __name__ == '__main__':
    unittest.main()
