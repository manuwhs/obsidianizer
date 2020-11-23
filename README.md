# obsidianizer
Library to enhance your knowledge base, especially designed to combine it [Obsidian vaults](https://obsidian.md/), adding advanced functionalities on top. 

# Features
Its main features are:
- Email journal logging: Write your thoughts during the day as entried in your email drafts. Then use obsidianizer to dump them into a latex file to be processed later.
- Latex processing: Load the journal entries previously stored ()
- Pdf processing: Automatically read the highlighed text and associated comments from your pdfs. You can then convert them to obsidian vaults.
- Obsidian vault processing: Load and create Vaults from your read pdfs and journals. Combine 
- NLP processing: The library comes with a set of functionalities to analyze the vaults. 


# Installation
```
pip install obsidianizer
```

# Examples

The [notebooks](./notebooks/) act as exmaples, documentation and test.

# Scripts 

The [scripts](./scripts/) folder contains a set of CLI utilities to make use of different utilities:
- [email_tools.pu](./scripts/email_tools.py): Tool to download emails in latex format.

## Setting up the environment
```
pip install obsidianizer
```

# Webapp 

A basic [webapp](./app/) has been developed to make use of the obsidian functionalities in a more user friendly manner. Not much time has been allocated to explain it. It is what it is.

# Run CI

The CI will run mypy and flake8 through the code
```
bash ci.sh
```

