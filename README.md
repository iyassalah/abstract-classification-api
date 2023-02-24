# abstract-classification-api
Back-end for the abstract classification app. 

## How to run
1. have python 3.11+ installed
2. pip install "fastapi[all]"
3. In the root directory, run `pip install -r requirements.txt` to install the dependancies.
4. Run `py -m uvicorn app.main:app --reload` to start the server process.

## Toolings
1. *Black* for formatting.
2. *mypy* for type-checking.
3. *pylint* for error and style linting.
4. *pylama*, because why not? 

## Tech
1. FastAPI and Pydantic
2. SKLearn

