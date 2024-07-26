# python-dev-environment
A skeleton environment for writing services using FastAPI and SQLAlchemy for data storage.

# Setup
Run `poetry install` before running the project. Remember also to select the correct Python interpreter in VS Code for debugging.

# Useful commands

* Run the development server: `poetry run fastapi dev python_service/main.py`
* Autoformat the code: `poetry run black python_service tests`
* Run unit tests: `poetry run pytest`

