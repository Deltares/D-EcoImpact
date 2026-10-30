FROM python:3.14-slim

LABEL org.opencontainers.image.source="https://github.com/Deltares/D-EcoImpact"

WORKDIR /decoimpact

# Copy files in local working directory to docker working directory
COPY . .

# Update the package source list, update system packages
RUN apt-get update && apt-get upgrade -y \
    && pip install uv

RUN uv sync \
    && apt-get clean autoclean

