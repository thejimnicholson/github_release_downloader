import codecs
import os.path
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

setup(
    name='github_release_downloader',
    version=get_version('github_release_downloader/_version.py'),
    url='https://github.com/thejimnicholson/github_release_downloader',
    author='Jim Nicholson',
    author_email='thejimnicholson@gmail.com',
    description='Download GitHub release assets specified in a YAML file.',
    packages=find_packages(),    
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'download-releases=github_release_downloader:main',
        ],
    },
)