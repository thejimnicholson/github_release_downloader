#!/usr/bin/env python

import os
import re
import yaml
import requests
import argparse

def get_releases(yaml_file_path=None, download_dir=None, base_url='https://api.github.com'):
  # If no YAML file path is provided, use the default file
  if yaml_file_path is None:
      yaml_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'github-releases.yaml')

  # If no download directory is provided, use the current working directory
  if download_dir is None:
    download_dir = os.getcwd()

  # Load the YAML file
  with open(yaml_file_path, 'r') as file:
    data = yaml.safe_load(file)

  # Iterate over each item in the YAML file
  for item in data:
    print(f"Looking at {item['name']}")

    # Get the latest release
    response = requests.get(f"{base_url}/repos/{item['repository']}/releases/latest")
    response.raise_for_status()
    json = response.json()

    # Print the name of the release
    print(f"Found release: {json['name']}")

    # Process the "files" attribute of the current item
    for file_pattern in item['files']:

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
            print(f"File {asset['name']} already exists and is the same size. Skipping download.")
          else:
            print(f"Downloading {asset['name']}")

            # Download the file
            response = requests.get(asset['browser_download_url'], stream=True)
            response.raise_for_status()

            # Save the file
            with open(local_file_path, 'wb') as file:
              for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Download GitHub release assets specified in a YAML file.')
  parser.add_argument('-c', '--config', help='Path to the YAML file.', default=None)
  parser.add_argument('-d', '--dir', help='Directory to download the files to.', default=None)
  parser.add_argument('-u', '--url', help='Base URL of the GitHub API server.', default='https://api.github.com')

  args = parser.parse_args()

  get_releases(args.config, args.dir, args.url)