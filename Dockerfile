FROM python:3.11-slim

LABEL org.opencontainers.image.source="https://github.com/Deltares/D-EcoImpact"

WORKDIR /decoimpact

# Copy files in local working directory to docker working directory
COPY . .

# Update the package source list, update system packages
RUN apt-get update && apt-get upgrade -y \
    && pip install poetry

# Install Poetry dependencies without creating poetry environment
## Packages are installed in "/usr/local/lib/python/site-packages/" when the environment is not created,
## which corresponds to the local installation of Python "/usr/local/bin/python" in the base Docker image
RUN poetry config virtualenvs.create false \
    && poetry install \
    && apt-get clean autoclean

