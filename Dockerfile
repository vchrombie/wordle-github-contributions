# Use a specific version to ensure consistency
FROM python:3.11-slim AS builder

# Set the working directory
ADD . /app
WORKDIR /app

# We are installing a dependency here directly into our app source dir
RUN pip install --target=/app requests python-dotenv

# Runtime image (keep Python version aligned with builder)
FROM python:3.11-slim
COPY --from=builder /app /app
WORKDIR /app
ENV PYTHONPATH /app
CMD ["python", "/app/src/main.py"]
