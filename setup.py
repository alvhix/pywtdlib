import pathlib
from setuptools import setup, find_packages
from pywtdlib import __version__

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="pywtdlib",
    version=__version__,
    author="alvhix",
    author_email="alvhix@gmail.com",
    description="A simple Python TDLib wrapper",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/alvhix/pywtdlib",
    project_urls={
        "Bug Tracker": "https://github.com/alvhix/pywtdlib/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.6",
)
