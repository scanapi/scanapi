# ScanAPI Development Container
FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

# Install additional system dependencies
RUN apt-get update && apt-get install -y \
  git \
  curl \
  build-essential \
  libssl-dev \
  zsh \
  && rm -rf /var/lib/apt/lists/*

# Install uv for faster package management
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Set environment variables
ENV PATH="$HOME/.cargo/bin:$PATH" \
  PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1

# Switch to vscode user for development
USER vscode
