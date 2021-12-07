import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pywtdlib",
    version="0.0.1",
    author="alvhix",
    author_email="alvhix@gmail.com",
    description="A simple Python TDLib wrapper",
    long_description=long_description,
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
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
