import argparse
import getpass
import os
import re
import sys

import requests
import yaml
from tqdm import tqdm

from github_release_downloader._version import __version__


def get_release_assets(yaml_file_path=None, 
                       download_dir=None, 
                       base_url='https://api.github.com', 
                       quiet=False,
                       show_progress=False):
  """
  Downloads the latest release assets from a GitHub repository.

  Parameters:
  yaml_file_path (str): The path to the YAML file that contains the repositories and files to download.
  download_dir (str): The directory where the downloaded files will be stored.
  base_url (str): The base URL for the GitHub API. Default is 'https://api.github.com'.
  quiet (bool): If set to True, the function will not print any output. Default is False.
  show_progress (bool): If set to True, the function will display a progress bar for the download. Default is False.

  The YAML file should have the following structure:
  - repository: The repository's name in the format 'username/repo'.
  - name: The name of the project.
  - files: A list of file patterns to match against the asset's name. Can be a string or a regex pattern.

  Example:
  - repository: 'username/repo'
    name: 'My Project'
    files: ['*.zip', 'README.md']

  This function will download the latest release assets that match the file patterns for each repository listed in the YAML file.
  If a local file with the same name and size already exists, the download is skipped.
  """

  # Suppress progress bars if quiet is set
  if quiet:
    show_progress=False

  # Load the YAML file
  with open(yaml_file_path, 'r') as file:
    data = yaml.safe_load(file)

  # Iterate over each item in the YAML file
  for item in data:

    # Get the latest release
    try:
      github_response = get_latest_release(item['repository'], base_url)
    except requests.exceptions.HTTPError as err:
      print(f"Error: received HTTP status {err.response.status_code} looking for latest release of {item['repository']}", file=sys.stderr)
      break

    # Print the name of the release
    if not quiet:
      print(f"Latest release of {item['name']} is {github_response['name']}")

    # Process the "files" attribute of the current item
    for file_pattern in item['files']:

      if not quiet:
        print(f" Looking for assets that match pattern {file_pattern}")

      # If the file pattern contains special regex characters, compile it as a regex
      if any(char in file_pattern for char in {'.', '^', '$', '*', '+', '?', '{', '}', '[', ']', '\\', '|', '(', ')'}):
        file_regex = re.compile(file_pattern)
        match_func = file_regex.match
      else:
        match_func = file_pattern.__eq__

      # Find the asset in the release
      for asset in github_response['assets']:
        if match_func(asset['name']):
          local_file_path = os.path.join(download_dir, asset['name'])

          # If the local file exists and its size is the same as the file to be downloaded, skip the download
          if os.path.exists(local_file_path) and os.path.getsize(local_file_path) == asset['size']:
            if not quiet:
              print(f"  File {asset['name']} already exists and is the same size. Skipping download.")
          else:
            if not quiet:
              print(f"  Downloading asset {asset['name']}")
            download_file(asset['browser_download_url'], local_file_path, show_progress)

def get_latest_release(repository, base_url='https://api.github.com'):
  """
  Fetches the latest release of a GitHub repository.

  Parameters:
  repository (str): The repository's name in the format 'username/repo'.
  base_url (str): The base URL for the GitHub API. Default is 'https://api.github.com'.

  Returns:
  dict: A dictionary containing the JSON response from the GitHub API.

  This function sends a GET request to the GitHub API to fetch the latest release of the specified repository.
  It raises an HTTPError if the request returns an unsuccessful status code.
  """
  response = requests.get(f"{base_url}/repos/{repository}/releases/latest")
  response.raise_for_status()
  return response.json()  

def download_file(url, local_file_path, show_progress):
  """
  Downloads a file from a given URL.

  Parameters:
  url (str): The URL of the file to download.
  local_file_path (str): The local path where the downloaded file will be saved.
  show_progress (bool): If set to True, the function will display a progress bar for the download.

  This function uses the requests library to download the file in chunks of 8192 bytes. 
  If show_progress is True, it uses the tqdm library to display a progress bar that shows how much of the file has been downloaded.
  The function raises an HTTPError if the download request returns an unsuccessful status code.
  """

  try:
      # Download the file
      response = requests.get(url, stream=True)
      response.raise_for_status()
  except requests.exceptions.HTTPError as err:
      if err.response.status_code == 404:
          print(f"Error: File not found at {url}")
          return
      else:
          raise

  # Get the total size of the file from the headers
  total_size = int(response.headers.get('content-length', 0))
  
  # Create a progress bar with tqdm
  if show_progress:
    progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)

  # Save the file
  with open(local_file_path, 'wb') as file:
    for chunk in response.iter_content(chunk_size=8192):
      if show_progress:
        progress_bar.update(len(chunk))
      file.write(chunk)

  # Close the progress bar
  if show_progress:
    progress_bar.close()


def main(argv=sys.argv):
  parser = argparse.ArgumentParser(description='Download GitHub release assets specified in a YAML file.')
  parser.add_argument('-c', '--config', help='Path to the YAML file.', default=os.path.join(os.getcwd(), 'github-releases.yaml'))
  parser.add_argument('-d', '--dir', help='Directory to download the files to.', default=os.getcwd())
  parser.add_argument('-u', '--url', help='Base URL of the GitHub API server.', default='https://api.github.com')
  parser.add_argument('-p', '--progress', help='Show download progress bar.', action='store_true')
  parser.add_argument('-q', '--quiet', help='Suppress all stdout print statements.', action='store_true')
  parser.add_argument('--version', action='version',
                   version='{version}'.format(version=__version__))

  args = parser.parse_args()

  if not os.path.exists(args.config):
    print(f"Error: Config file {args.config} does not exist.", file=sys.stderr)
    if not args.quiet:
      parser.print_help()
    sys.exit(1)

  # Check if the local file path exists and is writable
  if not os.path.exists(args.dir) or not os.access(args.dir, os.W_OK):
    print(f"Error: {args.dir} does not exist or is not writable by user {getpass.getuser()}.", file=sys.stderr)
    sys.exit(2)
  
  get_release_assets(args.config, args.dir, args.url, args.quiet, args.progress)

if __name__ == "__main__":
  main()