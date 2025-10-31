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
pip install git+https://github.com/thejimnicholson/github_release_downloader.git
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

This project is released under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

We welcome contributions to the GitHub Release Downloader project! Here's how you can help:

### Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/thejimnicholson/github_release_downloader.git
   cd github_release_downloader
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install the package in development mode:
   ```bash
   pip install -e .
   ```

### Making Changes

1. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes and add tests if applicable
3. Ensure your code follows Python style guidelines (PEP 8)
4. Test your changes thoroughly
5. Commit your changes with a descriptive commit message:
   ```bash
   git commit -m "Add feature: description of your changes"
   ```

### Testing

Before submitting your changes:

1. Run the tool with various configurations to ensure it works as expected
2. Test edge cases (missing files, network errors, permission issues)
3. Verify that existing functionality still works

### Submitting Changes

1. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
2. Create a Pull Request on GitHub with:
   - A clear title describing your changes
   - A detailed description of what you've changed and why
   - Any relevant issue numbers (e.g., "Fixes #123")

### Code Style

- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings for new functions
- Keep functions focused and relatively small
- Add comments for complex logic

### Reporting Issues

If you find a bug or have a feature request:

1. Check existing issues to avoid duplicates
2. Create a new issue with:
   - A clear, descriptive title
   - Steps to reproduce (for bugs)
   - Expected vs. actual behavior
   - Your environment details (OS, Python version, etc.)
   - Sample configuration files (if relevant)

### Questions?

Feel free to open an issue for questions about contributing or using the tool.

Thank you for contributing to make this project better!
