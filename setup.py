#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'dooble>=0.3',
]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Romain Picard",
    author_email='romain.picard@oakbits.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
    description="A sphinx extansion for dooble",
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords='dooble, sphinx',
    name='sphinxcontrib-dooble',
    packages=find_packages(),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/mainro/sphinxcontrib-dooble',
    version='1.0.0',
    zip_safe=True,
)
