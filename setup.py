# -*- coding: utf-8 -*-

# Python Package Setup
from setuptools import setup, find_namespace_packages

VERSION = "1.6.0"
DESCRIPTION = "A Python package to find the centerline and width of rivers based on the latitude and longitude of the right and left bank"

with open("README.md", "r") as f:
    long_description_readme = f.read()

setup(
    name="centerline-width",
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description_readme,
    long_description_content_type='text/markdown',
    url="https://github.com/cyschneck/centerline-width",
    download_url=
    f"https://github.com/cyschneck/centerline-width/archive/refs/tags/v{VERSION}.tar.gz",
    author="Una Schneck (unaschneck), Cora Schneck (cyschneck)",
    keywords=[
        "geophysics", "python", "voronoi", "networkx", "centerline",
        "centerline-extraction", "centerline-detection", "rivers",
        "river-bank-length", "river-bank", "limnology", "hydrology", "fluvial",
        "geomorphology"
    ],
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta", "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Hydrology",
        "Topic :: Scientific/Engineering :: Visualization"
    ],
    packages=find_namespace_packages(
        include=['centerline_width', 'centerline_width.*']),
    include_package_data=True,
    install_requires=[
        "geopy", "haversine", "matplotlib", "networkx", "numpy", "pandas",
        "pykml", "pyproj", "pytest", "scipy", "shapely"
    ],
    python_requires='>=3.9')
