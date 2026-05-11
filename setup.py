from setuptools import setup, find_packages

setup(
    name="h4md",
    version="0.1.1",
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
    author="IOWarp User",
    author_email="hyoklee@hdfgroup.org",
    url="https://github.com/hyoklee/h4md",
    description="A command-line tool to convert HDF4 datasets to markdown",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords="hdf4, markdown, conversion, hdf, data",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Utilities",
    ],
)
