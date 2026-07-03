FROM ubuntu:22.04

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    build-essential \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install HADDOCK3
RUN pip3 install --upgrade pip && \
    pip3 install haddock3

# Set working directory
WORKDIR /haddock_work

# Create necessary directories
RUN mkdir -p structures config results analysis

ENV PYTHONUNBUFFERED=1

CMD ["/bin/bash"]