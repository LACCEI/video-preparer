import unittest
from unittest.mock import patch, MagicMock
import hashlib
import time
import requests
import dataretriever

# class TestCTInterface(unittest.TestCase):
#     def test_generate_passhash(self):
#         nonce = dataretriever.generate_nonce()
#         passhash = dataretriever.generate_passhash(nonce)
#         self.assertEqual(len(passhash), 64)

#     def test_generate_nonce(self):
#         nonce = dataretriever.generate_nonce()
#         self.assertTrue(nonce.isdigit())

#     @patch('requests.get')
#     def test_send_get_request(self, mock_get):
#         url = 'http://test.com'
#         params = {'key': 'value'}
#         dataretriever.send_get_request(url, params)
#         mock_get.assert_called_once_with(url, params=params)

#     @patch('builtins.open', new_callable=unittest.mock.mock_open)
#     def test_save_file_from_response(self, mock_open):
#         mock_response = MagicMock()
#         mock_response.content = b'test content'
#         dataretriever.save_file_from_response(mock_response, 'test_file')
#         mock_open().write.assert_called_once_with(b'test content')

#     @patch('dataretriever.send_get_request')
#     def test_CTInterface_get_data(self, mock_get_request):
#         interface = dataretriever.CTInterface('http://test.com')
#         interface.get_data('export_select', 'output_file')
#         mock_get_request.assert_called_once_with('http://test.com', {
#             "page": "adminExport",
#             "export_select": 'export_select',
#             "format": 'xml'
#         })

# if __name__ == '__main__':
#     unittest.main()