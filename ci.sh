# echo "-------- black ------- "
black ./obsidianizer 
black ./tests
black ./app
echo  "-------- mypy ------- "
mypy ./obsidianizer ./tests ./app

echo "-------- flake8 ------- "
flake8 ./obsidianizer ./tests ./app

echo "-------- pytest ------- "
pytest 

echo "----- clean notebooks ----- "
jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace notebooks/documentation/*.ipynb
jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace notebooks/examples/*.ipynb