# -*- coding: utf-8 -*-

# Python Package Setup
from setuptools import setup, find_namespace_packages

VERSION="1.2.1"
DESCRIPTION="A Python package to find the centerline and width of rivers based on the latitude and longitude of the right and left bank"

with open("README.md", "r") as f:
	long_description_readme = f.read()

setup(
	name="centerline-width",
	version=VERSION,
	description=DESCRIPTION,
	long_description=long_description_readme,
	long_description_content_type='text/markdown',
	url="https://github.com/cyschneck/centerline-width",
	download_url="https://github.com/cyschneck/centerline-width/archive/refs/tags/v{0}.tar.gz".format(VERSION),
	author="Una Schneck (unaschneck), Cora Schneck (cyschneck)",
	keywords=["geophysics", "python", "voronoi", "networkx", "centerline", "centerline-extraction", "centerline-detection", "rivers", "river-bank-length", "river-bank", "limnology", "hydrology", "fluvial", "geomorphology"],
	license="MIT",
	classifiers=[
		"Development Status :: 3 - Alpha",
		"Intended Audience :: Developers",
		"Intended Audience :: Education",
		"Intended Audience :: Science/Research",
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python",
		"Programming Language :: Python :: 3.9",
		"Intended Audience :: Education",
		"Intended Audience :: Science/Research",
		"Topic :: Scientific/Engineering :: Physics",
		"Topic :: Scientific/Engineering :: Hydrology",
		"Topic :: Scientific/Engineering :: Visualization"
	],
	packages=find_namespace_packages(include=['centerline_width',
											'centerline_width.*']),
	include_package_data=True,
	install_requires=[
		"geopy>=2.3.0",
		"haversine>=2.8.0",
		"matplotlib>=3.1.0",
		"networkx>=3.0",
		"numpy>=1.24.1",
		"pandas>=1.3.5",
		"pykml>=0.2.0",
		"pyproj>=3.4.1",
		"pytest>=7.2.2",
		"scipy>=1.10.1",
		"shapely>=2.0.1"
	],
	python_requires='>=3.9'
)
