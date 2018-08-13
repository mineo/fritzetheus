#!/usr/bin/env python3
from __future__ import print_function
from codecs import open
from os import path
from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(name="fritzetheus",
      author="Wieland Hoffmann",
      author_email="themineo@gmail.com",
      packages=["fritzetheus"],
      package_dir={"fritzetheus": "fritzetheus"},
      download_url="https://github.com/mineo/fritzetheus/tarball/master",
      url="http://github.com/mineo/fritzetheus",
      license="MIT",
      classifiers=["Development Status :: 4 - Beta",
                   "License :: OSI Approved :: MIT License",
                   "Natural Language :: English",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python :: 3"],
      description="",
      long_description=long_description,
      long_description_content_type='text/markdown',
      python_requires='>=3.4.*',
      setup_requires=["setuptools_scm"],
      use_scm_version={"write_to": "fritzetheus/version.py"},
      extras_require={
          'docs': ['sphinx']
      }
      )
