FROM python:3.13-slim

WORKDIR /backend

# Install uv
# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates netcat-traditional 

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# RUN chmod +x /uv-installer.sh
# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"
# Set Python path
ENV PYTHONPATH=/backend

COPY requirements.in .

# Create a virtual environment and install the dependencies
# RUN uv venv
# RUN source .venv/bin/activate

RUN uv pip compile --system requirements.in -o requirements.txt && \
    uv pip sync --system requirements.txt

COPY . .


# Create a startup script
# COPY start.sh /start.sh
RUN chmod +x app/scripts/docker-entrypoint.sh

ENTRYPOINT ["/bin/sh", "app/scripts/docker-entrypoint.sh"]