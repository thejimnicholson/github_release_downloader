import argparse
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

  # Suppress progress bars if quiet is set
  if quiet:
    show_progress=False

  # Load the YAML file
  with open(yaml_file_path, 'r') as file:
    data = yaml.safe_load(file)

  # Iterate over each item in the YAML file
  for item in data:

    # Get the latest release
    response = requests.get(f"{base_url}/repos/{item['repository']}/releases/latest")
    response.raise_for_status()
    json = response.json()

    # Print the name of the release
    if not quiet:
      print(f"Latest release of {item['name']} is {json['name']}")

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
      for asset in json['assets']:
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


def download_file(url, local_file_path, show_progress):
  # Download the file
  response = requests.get(url, stream=True)
  response.raise_for_status()
  
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
    print(f"error: Config file {args.config} does not exist.", file=sys.stderr)
    if not args.quiet:
      parser.print_help()
    sys.exit(1)
  
  get_release_assets(args.config, args.dir, args.url, args.quiet, args.progress)

if __name__ == "__main__":
  main()