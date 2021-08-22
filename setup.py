#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = ['pandas>=1.1.0', 'numpy>=1.19.0', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Abuton",
    email="abubakarolayemi@gmail.org",
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A Repository that details how to get lidar data from USGS on AWS S3 bucket",
    install_requires=requirements,
    long_description=readme,
    include_package_data=True,
    keywords='lidardataextractor',
    name='get_data',
    packages=find_packages(include=['lidardataextractor', 'lidardataextractor.*']),
    test_suite='tests',
    url='https://github.com/Abuton/lidarDataExtractor',
    version='0.1.0',
    zip_safe=False,
)
