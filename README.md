# abstract-classification-api

Back-end for the abstract classification app.

## How to run

1. Have python 3.11+ installed
2. Create and activate a virtual environment with `venv`
3. Run `pip install "fastapi[all]"` to install FastAPI and Uvicorn
4. In the root directory, run `pip install -r requirements.txt` to install the dependancies.
5. Run `py -m uvicorn app.main:app --reload` to start the server process.

## Tooling

1. *Black* for formatting.
2. *mypy* for type-checking.
3. *pylint* for error and style linting.
4. *pylama*, because why not?
5. *venv*

## Tech stack

1. FastAPI and Pydantic
2. SKLearn
3. MongoDB
