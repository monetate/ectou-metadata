#!/usr/bin/env python

from setuptools import setup


setup(
    name="ectou-metadata",
    version="1.0.2",
    description="Yet another EC2 instance metadata mocking service.",
    url="https://github.com/monetate/ectou-metadata",
    author='Monetate',
    author_email='jjpersch@monetate.com',
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
    ],
    keywords="aws instance metadata",
    packages=[
        'ectou_metadata',
    ],
    install_requires=[
        "boto3",
        "bottle",
    ],
    entry_points={
        'console_scripts': [
            'ectou_metadata = ectou_metadata.service:main',
        ],
    },
    test_suite="tests",
)
