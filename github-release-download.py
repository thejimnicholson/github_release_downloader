#!/usr/bin/env python

import requests
import yaml
import os

# Load the YAML file
with open('github-releases.yaml', 'r') as file:
  data = yaml.safe_load(file)

# For each item in the YAML file
for item in data:
  print(f"Looking at {item['name']}")
  # Get the latest release
  response = requests.get(f"https://api.github.com/repos/{item['repository']}/releases/latest")
  response.raise_for_status()
  json = response.json()

  # Print the name of the release
  print(f"Found release: {json['name']}")

  # For each file we want to download
  for file_name in item['files']:

    # Find the asset in the release
    for asset in json['assets']:
      
      if asset['name'] == file_name:
        local_file_path = f'github-release-downloads/{file_name}'
              # If the local file exists and its size is the same as the file to be downloaded, skip the download
        if os.path.exists(local_file_path) and os.path.getsize(local_file_path) == asset['size']:
          print(f"File {file_name} already exists and is the same size. Skipping download.")
        else:
          print(f"Downloading {asset['name']}")
          # Download the file
          response = requests.get(asset['browser_download_url'], stream=True)
          response.raise_for_status()

          # Save the file
          with open(f"github-release-downloads/{file_name}", 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
              file.write(chunk)
          break