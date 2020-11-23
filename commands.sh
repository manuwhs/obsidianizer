# packages to install
sudo apt install python-pip
sudo apt-get install python3-venv
python3 -m pip install --user virtualenv

# Create virtual environment
python3 -m venv obsidianizer_env
source obsidianizer_env/bin/activate

# Special installation 
sudo -H obsidianizer_env/bin/pip3 install --upgrade pip
sudo -H obsidianizer_env/bin/pip3 install -U pymupdf

# Install the library
git clone XXX 
cd XXX
pip install -e .

# Download additional packages.
python -m spacy download es
python -m spacy download en
python -m spacy download en_core_web_md

pip install pyspellchecker
pip install -U sentence-transformers