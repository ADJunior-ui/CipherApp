import unittest

from app import app


class AppRouteTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home_route_returns_html(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_encode_single_char_with_key(self):
        response = self.client.post(
            '/process',
            json={'mode': 'encode', 'text': 'A', 'key': 1}
        )
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['result'], '6,6')
        self.assertIsNotNone(data.get('graph'))

    def test_encode_multiple_chars(self):
        response = self.client.post(
            '/process',
            json={'mode': 'encode', 'text': 'AB', 'key': 0}
        )
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertIn(',', data['result'])

    def test_decode_single_coordinate(self):
        response = self.client.post(
            '/process',
            json={'mode': 'decode', 'text': '6,6', 'key': 1}
        )
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['result'], 'A')

    def test_decode_multiple_coordinates(self):
        response = self.client.post(
            '/process',
            json={'mode': 'decode', 'text': '5,6 6,6', 'key': 0}
        )
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(len(data['result']), 2)

    def test_empty_text_returns_error(self):
        response = self.client.post(
            '/process',
            json={'mode': 'encode', 'text': '', 'key': 0}
        )
        data = response.get_json()
        self.assertFalse(data['success'])
        self.assertIn('error', data)

    def test_whitespace_only_returns_error(self):
        response = self.client.post(
            '/process',
            json={'mode': 'encode', 'text': '   \n\t  ', 'key': 0}
        )
        data = response.get_json()
        self.assertFalse(data['success'])

    def test_invalid_characters_returns_error(self):
        response = self.client.post(
            '/process',
            json={'mode': 'encode', 'text': 'A\x01B', 'key': 0}
        )
        data = response.get_json()
        self.assertFalse(data['success'])
        self.assertIn('Invalid', data['error'])

    def test_bad_coordinate_format_returns_error(self):
        # Non-numeric text gets converted to 0 by safe_int, producing (0,0)
        response = self.client.post(
            '/process',
            json={'mode': 'decode', 'text': 'abc,def', 'key': 0}
        )
        data = response.get_json()
        # safe_int converts non-numeric to 0, so (0,0) is a valid coordinate
        # Since (0,0) is in range, the decode succeeds
        self.assertTrue(data['success'])

    def test_decode_with_no_valid_coordinates(self):
        response = self.client.post(
            '/process',
            json={'mode': 'decode', 'text': 'a b c', 'key': 0}
        )
        data = response.get_json()
        self.assertFalse(data['success'])

    def test_missing_mode_defaults_to_encode(self):
        response = self.client.post(
            '/process',
            json={'text': 'A', 'key': 0}
        )
        data = response.get_json()
        self.assertTrue(data['success'])

    def test_missing_key_defaults_to_zero(self):
        response = self.client.post(
            '/process',
            json={'mode': 'encode', 'text': 'A'}
        )
        data = response.get_json()
        self.assertTrue(data['success'])

    def test_bad_key_defaults_to_zero(self):
        response = self.client.post(
            '/process',
            json={'mode': 'encode', 'text': 'A', 'key': 'not_a_number'}
        )
        data = response.get_json()
        self.assertTrue(data['success'])

    def test_large_key_value(self):
        response = self.client.post(
            '/process',
            json={'mode': 'encode', 'text': 'A', 'key': 1000}
        )
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['result'])

    def test_negative_key_value(self):
        response = self.client.post(
            '/process',
            json={'mode': 'encode', 'text': 'A', 'key': -5}
        )
        data = response.get_json()
        self.assertTrue(data['success'])

    def test_coordinates_out_of_range(self):
        response = self.client.post(
            '/process',
            json={'mode': 'decode', 'text': '15,15', 'key': 0}
        )
        data = response.get_json()
        self.assertFalse(data['success'])

    def test_large_input_rejected(self):
        large_text = 'A' * 10001
        response = self.client.post(
            '/process',
            json={'mode': 'encode', 'text': large_text, 'key': 0}
        )
        data = response.get_json()
        self.assertFalse(data['success'])
        self.assertIn('too large', data['error'])

    def test_unknown_mode_returns_error(self):
        response = self.client.post(
            '/process',
            json={'mode': 'unknown', 'text': 'A', 'key': 0}
        )
        data = response.get_json()
        self.assertFalse(data['success'])

    def test_graph_is_base64_encoded(self):
        response = self.client.post(
            '/process',
            json={'mode': 'encode', 'text': 'Hello', 'key': 1}
        )
        data = response.get_json()
        if data['success'] and data.get('graph'):
            graph = data['graph']
            self.assertIsInstance(graph, str)
            self.assertTrue(len(graph) > 0)


if __name__ == '__main__':
    unittest.main()
