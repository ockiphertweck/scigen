FROM python:3.11-slim

# Install Poetry
RUN pip install poetry

# Configure Poetry to not create virtual environments
RUN poetry config virtualenvs.create false

# Set the working directory
WORKDIR /code

# Copy necessary files
COPY ./pyproject.toml ./README.md ./


# Install dependencies without the root package
RUN poetry install --no-interaction --no-ansi --no-root

# Copy the application files
COPY ./app ./app

# Install the application
RUN poetry install --no-interaction --no-ansi

# Expose the port
EXPOSE 8000

# Command to run the application
CMD poetry run serve
