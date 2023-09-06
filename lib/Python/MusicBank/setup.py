import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION      = '0.2'
PACKAGE_NAME = 'MusicBank'
AUTHOR       = 'Josef Grosch'
AUTHOR_EMAIL = 'jgrosch@gmail.com'
URL          = 'https://github.com/jgrosch510/MusicBank'

LICENSE = 'BSD 2-clause "Simplified" license'
DESCRIPTION = 'Describe your package in one sentence'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
    'numpy',
    'pandas',
    'musicbrainzngs'
]

setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      url=URL,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages()
      )

