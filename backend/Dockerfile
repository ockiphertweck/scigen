FROM python:3.11-slim

# Install Poetry
RUN pip install poetry

# Configure Poetry to not create virtual environments
RUN poetry config virtualenvs.create false

# Set the working directory
WORKDIR /code

# Copy necessary files
COPY ./pyproject.toml ./README.md ./

# Copy the packages directory
COPY ./packages ./packages

# Install dependencies without the root package
RUN poetry install --no-interaction --no-ansi --no-root

# Copy the application files
COPY ./app ./app

# Debug: List files in the /code directory and /code/app
RUN ls -la /code
RUN ls -la /code/app

# Install the application
RUN poetry install --no-interaction --no-ansi

# Expose the port
EXPOSE 8000

# Command to run the application
CMD poetry run serve
