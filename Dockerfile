FROM python:3.9-slim-buster

# Set environment variables
ENV PYTHONUNBUFFERED=1
ARG DATABASE_URL
ENV DATABASE_URL=$DATABASE_URL


# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY ./app ./app
# Copy alembic configuration and migrations
COPY alembic.ini .
COPY migrations migrations

# Copy the entrypoint script
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Expose port
EXPOSE 8000

# Run the application with the correct module path
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
ENTRYPOINT ["./entrypoint.sh"]
