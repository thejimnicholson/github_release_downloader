FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create a user with UID 1000 and GID 1000
RUN groupadd -g 1000 appuser && \
    useradd -r -u 1000 -g appuser appuser

# Copy the application files
COPY . .

# Install the package
RUN pip install --no-cache-dir .

# Create a directory for downloads and set ownership
RUN mkdir -p /downloads && \
    chown -R appuser:appuser /downloads

# Switch to the non-root user
USER appuser

# Set the default working directory for downloads
WORKDIR /downloads

# Set the entrypoint to the download-releases command
ENTRYPOINT ["download-releases"]

# Default command (can be overridden)
CMD ["--help"]