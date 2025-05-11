from setuptools import setup, find_packages

setup(
    name="h4md",
    version="0.1.0",
    packages=find_packages(),
    py_modules=["h4md"],
    install_requires=[
        "pyhdf>=0.10.5",
        "click>=8.1.0",
    ],
    entry_points={
        "console_scripts": [
            "h4md=h4md:main",
        ],
    },
    author="Your Name",
    description="A command-line tool to convert HDF4 datasets to markdown",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords="hdf4, markdown, conversion",
    python_requires=">=3.6",
)
