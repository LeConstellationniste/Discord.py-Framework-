"""
setup.py for the project 'discordEasy'.

Authors: LostPy & LeConstéllationniste
"""

from setuptools import setup, find_packages

import discordEasy


__doc__ = """A package to make functional Bot discord very easily and quickly."""
__license__ = "CC0 1.0 Universal"


setup(
	name='discordEasy',
	version='1.20210130',
	author='LostPy & LeConstéllationniste',
	description="A package to make functional Bot discord very easily and quickly.",
	long_description=__doc__,
    package_dir = {'discordEasy': './discordEasy'},
    package_data = {'': ['LICENSE.txt']},
	include_package_data=True,
	url='https://github.com/LeConstellationniste/Discord.py-Framework-',
	classifiers=[
        "Programming Language :: Python",
        "Development Status :: In progress",
        f"License :: {__license__}",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5+",
        "Topic :: discord",
    ],
    license=__license__,
    packages = find_packages()
    )
