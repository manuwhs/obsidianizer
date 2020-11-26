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
