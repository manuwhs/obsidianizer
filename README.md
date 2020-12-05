# obsidianizer
Library to enhance your [Obsidian vaults](https://obsidian.md/) knowledge base.

# Features

Obsidianier offers a set of advanced features to create and process Obsidian vaults, these include:
- **Email journal logging**: Write your thoughts during the day as entried in your email drafts. Then use obsidianizer to dump them into a latex file to be processed later.
- **Latex processing**: Load the journal entries previously stored ()
- **Pdf processing**: Automatically read the highlighed text and associated comments from your pdfs. You can then convert them to obsidian vaults.
- **Obsidian vault** processing: Load and create Vaults from your read pdfs and journals. Combine 
- **NLP processing**: The library comes with a set of functionalities to analyze the vaults. 


# Installation

This repo is not in [pypi](https://pypi.org/) yet. It requires the installation of other tools and models to be executed. The [bootstrap_environment.sh](./bootstrap_environment.sh) file contains the set of command line instructions to set a development environment from scratch in Ubuntu. Please feel free to cherry pick the parts you need.

``` bash
# Packages related to python to install
sudo apt install python-pip
sudo apt-get install python3-venv
python3 -m pip install --user virtualenv

# Create virtual environment
python3 -m venv obsidianizer_env
source obsidianizer_env/bin/activate
pip3 install --upgrade pip

# Install numba for later package installation
pip3 install numba 

# We need to install pymupdf this way first
pip3 install -U pymupdf

# Install the obsidianizer library
git clone https://github.com/manuwhs/obsidianizer.git 
cd obsidianizer
pip3 install -e .   # Install in development mode.

# Download additional packages for different advanced libraries
python -m spacy download es
python -m spacy download en
python -m spacy download en_core_web_md
python -m spacy download es_core_news_md

pip3 install pyspellchecker
pip3 install -U sentence-transformers
```

# Examples

The [notebooks](./notebooks/) act as exmaples, documentation and test. The best way to become familiar with the API and its functionalities is to execute the [documentation notebooks](./notebooks/documentation) in order. 


# Scripts 

The [scripts](./scripts/) folder contains a set of CLI utilities. Most of the functionalities of this repo are accessed through the notebooks and the webapp as they require more complex inputs. These utilities contain simple specific use cases:

- [email_tools.py](./scripts/email_tool.py): Tool to mainly download emails in latex format.


# Webapp 

A basic [webapp](./app/) has been developed to make use of the obsidian functionalities in a more user friendly manner. Not much time has been allocated to explain it. It is what it is for now. In order to execute it, chage directory to the [app](./app/) folder and execute the main.py file:

```
cd app
python3 main.py
```

# Run CI

The CI pipeline will:
    - Format the code and look for inconsistencies: It uses black, mypy and flake8.
    - Run tests: It will run the notebooks in 
    - It will clean the cells of all notebooks so that they are cleared before commiting the code.

```
bash ci.sh
```

# DISCLAIMER: So far this repo does not contain the test data as it is private. In the future it will be replace with public information.
