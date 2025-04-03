# Use an official base image with your desired version
FROM ollama/ollama:latest

ENV PYTHONUNBUFFERED=1 

# Set up the working directory
WORKDIR /

RUN apt-get update --yes --quiet && DEBIAN_FRONTEND=noninteractive apt-get install --yes --quiet --no-install-recommends \
    software-properties-common \
    gpg-agent \
    build-essential apt-utils \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get install --reinstall ca-certificates

# PYTHON 3.10
RUN add-apt-repository --yes ppa:deadsnakes/ppa && apt update --yes --quiet

RUN DEBIAN_FRONTEND=noninteractive apt-get install --yes --quiet --no-install-recommends \
    python3.11 \
    python3.11-dev \
    python3.11-distutils \
    python3.11-lib2to3 \
    python3.11-gdbm \
    python3.11-tk \
    pip

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 999 \
    && update-alternatives --config python3 && ln -s /usr/bin/python3 /usr/bin/python

RUN pip install --upgrade pip

# Add your file
ADD . .

RUN pip install runpod

# Override Ollama's entrypoint
ENTRYPOINT ["bin/bash", "start.sh"]

CMD ["mistral"]