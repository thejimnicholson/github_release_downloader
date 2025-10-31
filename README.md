# GitHub Release Downloader

A Python command-line tool for downloading release assets from GitHub projects based on configurable patterns.

## Overview

This tool helps you maintain a curated collection of GitHub-hosted tools by automatically downloading the latest release assets that match your specified patterns. It's particularly useful when:

- Working behind corporate firewalls where traditional package managers are restricted
- Building internal software distributions for your team
- Automating the collection of specific release artifacts from multiple repositories
- Maintaining consistent tool versions across development environments

## Features

- **Pattern Matching**: Download assets using glob patterns or regular expressions
- **Bulk Downloads**: Process multiple repositories from a single YAML configuration file
- **Smart Caching**: Skip downloads if local files already exist and match the expected size
- **Progress Tracking**: Optional progress bars for download monitoring
- **GitHub API Integration**: Support for personal access tokens to increase rate limits and access private repositories
- **Quiet Mode**: Suppress output for automated workflows

## Installation

```bash
pip install .
```

Or install directly from the repository:

```bash
pip install git+https://github.com/yourusername/github_release_downloader.git
```

## Quick Start

1. Create a YAML configuration file (`github-releases.yaml`):

```yaml
- repository: 'cli/cli'
  name: 'GitHub CLI'
  files: ['*linux_amd64.tar.gz']

- repository: 'docker/compose'
  name: 'Docker Compose'
  files: ['docker-compose-linux-x86_64']
```

2. Run the downloader:

```bash
download_releases -c github-releases.yaml -d ./downloads
```

## Usage

```bash
download_releases [OPTIONS]
```

### Options

- `-c, --config PATH`: Path to YAML configuration file (default: `github-releases.yaml`)
- `-d, --dir PATH`: Download directory (default: current directory)
- `-u, --url URL`: GitHub API base URL (default: `https://api.github.com`)
- `-t, --token TOKEN`: GitHub personal access token for authentication
- `-p, --progress`: Show download progress bars
- `-q, --quiet`: Suppress all output messages
- `-h, --help`: Show help message

### Configuration File Format

The YAML configuration file should contain a list of repositories with the following structure:

```yaml
- repository: 'owner/repo'    # Required: GitHub repository in 'owner/repo' format
  name: 'Project Name'        # Required: Human-readable name for the project
  files:                      # Required: List of file patterns to download
    - '*.zip'                 # Glob pattern
    - 'binary-linux-.*'       # Regular expression (auto-detected)
    - 'specific-file.tar.gz'  # Exact filename
```

### Examples

Download with progress bars:
```bash
download_releases --config tools.yaml --dir ./bin --progress
```

Use with GitHub token for higher rate limits:
```bash
download_releases --token ghp_xxxxxxxxxxxx --config private-repos.yaml
```

Silent operation for scripts:
```bash
download_releases --quiet --config automation.yaml
```

## Pattern Matching

The tool supports both simple glob patterns and regular expressions:

- **Simple patterns**: `*.zip`, `*linux*`, `binary-*`
- **Regex patterns**: Automatically detected when special regex characters are present
- **Exact matches**: `specific-filename.tar.gz`

## Authentication

For private repositories or to increase API rate limits, use a GitHub personal access token:

1. Generate a token at https://github.com/settings/tokens
2. For public repositories: No specific scopes required
3. For private repositories: Grant `repo` scope
4. Use with `--token` flag or set `GITHUB_TOKEN` environment variable

## Error Handling

The tool gracefully handles common scenarios:

- **Missing files**: Continues processing other assets if a specific file isn't found
- **Network issues**: Displays clear error messages for connection problems
- **Permission errors**: Exits with appropriate error codes for file system issues
- **API rate limits**: Use authentication tokens to avoid rate limiting

## Requirements

- Python 3.6+
- `requests` library
- `PyYAML` library
- `tqdm` library (for progress bars)

## License

[Add your license information here]

## Contributing

[Add contributing guidelines here]
