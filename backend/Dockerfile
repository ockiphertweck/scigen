FROM python:3.11-slim

RUN pip install poetry

RUN poetry config virtualenvs.create false

WORKDIR /code

# Copy the necessary files
COPY ./pyproject.toml ./README.md ./poetry.lock* ./
COPY ./packages ./packages

# Install the dependencies
RUN poetry install --no-interaction --no-ansi --no-root

# Copy the application files
COPY ./app ./app

# Install the application
RUN poetry install --no-interaction --no-ansi

EXPOSE 8080

# Command to run the application
CMD poetry run serve
