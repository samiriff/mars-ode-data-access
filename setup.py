#!/usr/bin/env python
# coding=utf-8

import os
import io

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as fp:
    README = fp.read()

# this module can be zip-safe if the zipimporter implements iter_modules or if
# pkgutil.iter_importer_modules has registered a dispatch for the zipimporter.
try:
    import pkgutil
    import zipimport
    zip_safe = hasattr(zipimport.zipimporter, "iter_modules") or \
        zipimport.zipimporter in pkgutil.iter_importer_modules.registry.keys()
except (ImportError, AttributeError):
    zip_safe = False

setup(
    name='mars-ode-data-access',
    version='0.1.0',
    description="ODE Data Access is a utility that allows users to download data from the Orbital Data Explorer",
    long_description=README,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Scientific/Engineering :: Image Segmentation",
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='mars ode nasa mro hirise jp2 lbl chunks',
    author='samiriff',
    author_email='samiriff@gmail.com',
    url='https://github.com/samiriff/mars-ode-data-access',
    download_url='https://github.com/samiriff/mars-ode-data-access/archive/0.1.0.tar.gz',
    license='MIT License',
    packages=find_packages(exclude=["docs", "tests", "tests.*"]),
    platforms=["any"],
    zip_safe=zip_safe,
    python_requires=">=3.4",
    install_requires=[
        "fastai",
        "matplotlib",
        "numpy",
        "rasterio",
        "scikit-dataaccess",
        "scikit-learn",
        "tqdm",
    ],
)