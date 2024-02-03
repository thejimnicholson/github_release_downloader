import unittest
from unittest.mock import patch
from github_release_downloader import get_releases

class TestGetReleases(unittest.TestCase):
    @patch('requests.get')
    def test_get_releases(self, mock_get):
        # Mock the response from requests.get
        mock_response = mock_get.return_value
        mock_response.json.return_value = [
            {'name': 'release1'},
            {'name': 'release2'},
            {'name': 'release3'},
        ]

        # Call the function with a fake repository
        get_releases('fake_repo')

        # Assert that requests.get was called with the correct URL
        mock_get.assert_called_once_with('https://api.github.com/repos/fake_repo/releases')



if __name__ == '__main__':
    unittest.main()