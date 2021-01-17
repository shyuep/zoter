# coding: utf-8

from setuptools import setup, find_packages

setup(
    name="zoter",
    packages=find_packages(),
    version="2021.1.17",
    setup_requires=['setuptools>=43.0.0'],
    python_requires='>=3.7',
    install_requires=["requests"],
    author="Shyue Ping Ong",
    author_email="shyuep@gmail.com",
    maintainer="Shyue Ping Ong",
    maintainer_email="shyuep@gmail.com",
    license="BSD",
    description="Zoter is an interface to the Zotero API.",
    long_description="Zoter is an interface to the Zotero API.",
    long_description_content_type='text/markdown',
    keywords=["zotero", "api"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    entry_points={
        'console_scripts': [
            'zot2nsf = zoter.cli.zot2nsf:main',
        ]
    }
)
