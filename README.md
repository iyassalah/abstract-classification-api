# abstract-classification-api

Back-end for the abstract classification app.

## Configuations

The project is configured using `.env` files, the priority is as follows:

1. `.env.dev.local` / `.env.prod.local`
2. `.env.local`
3. `.env.dev` / `.env.prod`
4. `.env`
5. System environment variables

Local config files are ignored by git, a priority flag is added to some files to indicate which file contributed which values, for debugging purposes.

## How to run

1. Have python 3.11+ installed
2. Create and activate a virtual environment with `venv`
3. Run `pip install "fastapi[all]"` to install FastAPI and Uvicorn
4. In the root directory, run `pip install -r requirements.txt` to install the dependancies.
5. Run `python -m uvicorn app.main:app --reload` to start the server process, simply run [this script]('./dev.bat') from the terminal.

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
