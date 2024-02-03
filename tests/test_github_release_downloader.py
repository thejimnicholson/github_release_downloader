import unittest
import os
from unittest.mock import patch, mock_open
from github_release_downloader import get_releases  # replace with the name of your script

class TestGithubReleaseDownload(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open, read_data="files:\n- file1\n- file2")
    @patch('os.path.exists', return_value=True)
    @patch('os.path.getsize', return_value=123)
    @patch('requests.get')
    def test_github_release_download(self, mock_get, mock_getsize, mock_exists, mock_yaml):
        mock_response = mock_get.return_value
        mock_response.iter_content.return_value = [b'file content']
        mock_response.raise_for_status.return_value = None

        get_releases('fake_path')

        mock_get.assert_called()
        mock_getsize.assert_called()
        mock_exists.assert_called()
        mock_yaml.assert_called_with('fake_path', 'r')

if __name__ == '__main__':
    unittest.main()