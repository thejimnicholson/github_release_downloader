from setuptools import setup, find_packages

setup(
    name='github_release_downloader',
    version='0.1.0',
    url='https://github.com/thejimnicholson/github_release_downloader',
    author='Jim Nicholson',
    author_email='thejimnicholson@gmail.com',
    description='Download GitHub release assets specified in a YAML file.',
    packages=find_packages(),    
    install_requires=[],
)