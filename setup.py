#!/usr/bin/env python

from setuptools import setup

install_requires = [
    "requests>=2.10.0",
    "BeautifulSoup>=3.2.1"
]

setup(
    name='Embeddit',
    version='1.0',
    description='A simple oembed meta fetcher which falls back to open graph info when oembed is not available.',
    author='Ryan Nagle',
    author_email='rmnagle@gmail.com',
    license='MIT',
    url='https://github.com/rnagle/embeddit',
    packages=['embeddit'],
    install_requires=install_requires
)
