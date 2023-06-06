from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in bookhotel/__init__.py
from bookhotel import __version__ as version

setup(
	name="bookhotel",
	version=version,
	description="Application for hotel booking",
	author="Cargoshare",
	author_email=".",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
