from setuptools import setup, find_packages

setup(
    name="cloudstor-downloader",
    version="0.1.0",
    author="Daniel Axford",
    author_email="daxford@murdoch.edu.au",
    description="A tool for downloading files from Cloudstor",
    packages=find_packages(),
    install_requires=[
        "cloudstor",
        "tqdm"
    ],
)
