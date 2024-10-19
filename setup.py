#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# based on: https://github.com/brainelectronics/micropython-package-template

from setuptools import setup
from pathlib import Path
import sdist_upip

here = Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

# load elements of version.py
exec(open(here / 'src' / 'RPIoTlogger' / 'version.py').read())

setup(
    name='RPIoTlogger',
    version=__version__,
    description='Raspberry Pi PicoW to get sensor output and post API for InfluxDB',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/atsuyaw/RPIoTlogger',
    author='atsuyaw',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: MIT License',
        'Programming Language :: Python :: Implementation :: MicroPython',
    ],
    # keywords='',
    package_dir={'src'},
    project_urls={
        # 'Bug Reports': '',
        'Repository': 'https://github.com/atsuyaw/RPIoTlogger',
    },
    license='MIT',
    cmdclass={'sdist': sdist_upip.sdist},
    packages=setup.find_packages(where='src'),
    install_requires=['onewire']
)
