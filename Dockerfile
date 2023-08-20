# Stage 1: Base
FROM python:3.8-slim as base

# Create and set up the appuser
RUN useradd -ms /bin/bash appuser
ARG HOME=/home/appuser
WORKDIR ${HOME}
RUN chown -R appuser:appuser ${HOME}

# Change to the appuser
USER appuser

# Copy cloud files
COPY --chown=appuser:appuser pyproject.toml poetry.lock ./
COPY --chown=appuser:appuser src ./src

# Set environment variables
ENV PORT 8000
ENV PYTHONUNBUFFERED True
ENV PATH="${HOME}/.local/bin:${PATH}"

# Install Poetry
RUN pip install poetry

# Stage 2: Development
FROM base as dev

# Copy additional files for development
COPY --chown=appuser:appuser tests/ ./tests

# Install project dependencies using Poetry
RUN poetry install

# Set default command for development
CMD exec poetry run uvicorn --root-path ${HOME}/src src.main:app --reload --host 0.0.0.0 --port ${PORT}

# Stage 3: Production
FROM base as prod

# Set number of workers for production
ENV WORKERS 4

# Install project dependencies using Poetry (without dev dependencies)
RUN poetry install --no-dev

# Set default command for production
CMD exec poetry run gunicorn --chdir ${HOME}/src main:app --workers ${WORKERS} -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:${PORT} --timeout 600
