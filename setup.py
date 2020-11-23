# Always prefer setuptools over distutils
from setuptools import find_packages, setup

# Get the long description from the README file
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", "r") as requirements_file:
    requirements = requirements_file.read().split("\n")
    requirements = [rec for rec in requirements if len(rec) > 0 and rec[0] != "#"]

setup(
    name="obsidianizer",
    version="0.0.1",
    description="Utilities to convert annotated pdfs to obsidian files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    author="Manuel Montoya",
    author_email="manuwhs@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
    ],
    keywords="Utilities to convert annotated pdfs to obsidian files",
    packages=find_packages(),
    setup_requires=requirements,  # >38.6.0 needed for markdown README.md
    install_requires=requirements,
)
