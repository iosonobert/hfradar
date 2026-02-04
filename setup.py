#!/usr/bin/env python

from setuptools import setup, find_packages
from setuptools.dist import Distribution

class BinaryDistribution(Distribution):
    def is_pure(self):
        return False

		
setup(name='hfradar',
      version='0.1.1',
      description='High Frequency Radar Data Processing Library',
      author='Andrew Zulberti',
      author_email='andrew.zulberti@gmail.com',
      packages=find_packages(),
      install_requires=['numpy',
                        'matplotlib', 
                        'netcdf4', 
                        'scipy',
                        'xarray',
                        'utm',
                        'pyshp',
                        'gpxpy'],
      license='unlicensed to all but author',
      include_package_data=True,
      distclass=BinaryDistribution,
    )
