# E-Commerce RESTful API

This project implements a RESTful API with FastAPI and SQLAlchemy (Postgres) for a simple e-commerce platform. It allows users to view products, add new products, and place orders.

## Features

- **GET /products:** Retrieves a list of all available products.
- **POST /products:** Adds a new product to the platform.
- **POST /orders:** Places an order for selected products, with stock validation.
- **Data Models:** Product and Order models with defined fields.
- **Stock Management:** Validates and deducts stock when orders are placed.
- **Order Validation:** Ensures sufficient stock before confirming orders.
- **Exception Handling:** Graceful error handling with meaningful responses.
- **Testing:** Comprehensive unit and integration tests.
- **Dockerization:** Containerized environment for easy deployment.

## Prerequisites

- Docker and Docker Compose installed.
- Python 3.9+ installed (for local development and testing).
- pip installed.
- virtualenv or conda installed (optional, but recommended).

## Getting Started

### 1. Clone the Repository

```bash
git clone <your_repository_url>
cd <your_repository_directory>
```

### 2. Set Up Environment Variables
Create a .env file in the project root directory with the following content:

DATABASE_URL=postgresql://ecommerce_user:ecomdb@db/ecommerce_db
### 3. Build and Run the Docker Containers
```bash
docker-compose up --build -d
```
```bash
docker run -p 8080:8000 ecomm-api (your image name)
```
This command will:

Build the Docker image for the application.
Start the PostgreSQL database container.
Start the application container.
Run Alembic migrations to create the database schema.
```bash
docker-compose exec app alembic revision --autogenerate -m "Initial migration: Create tables"
docker-compose exec app alembic upgrade head
```
## 4. Access the API
The API will be available at http://localhost:8000.

API Documentation: Access the interactive API documentation at http://localhost:8000/docs.(Swagger -Fast API)
## 5. Testing
Running Tests Inside Docker
To run the tests within the Docker container:
```bash
docker-compose exec app pytest
```

Running Tests Locally (Optional)
If you wish to run the tests locally, set up a virtual environment, install dependencies, and run pytest.

```bash

python3 -m venv venv
source venv/bin/activate  # On Linux/macOS
# venv\Scripts\activate  # On Windows
pip install -r requirements.txt
pytest

```

Ensure a postgres instance is running locally, and that the .env.local file is configured correctly.

```bash
6. Stopping the Containers
To stop the Docker containers:
```
```bash

docker-compose down

```
API Endpoints
GET /products
Retrieves a list of all available products.
Example Request:

GET http://localhost:8000/products
Example Response:

```JSON

[
  {
    "id": 1,
    "name": "Example Product",
    "description": "This is an example product.",
    "price": 29.99,
    "stock": 100
  },
 
]
```
POST /products
Adds a new product to the platform.

Example Request:

POST http://localhost:8000/products
Content-Type: application/json

{
  "name": "New Product",
  "description": "A brand new product.",
  "price": 49.99,
  "stock": 50
}
Example Response:
```json
{
  "id": 2,
  "name": "New Product",
  "description": "A brand new product.",
  "price": 49.99,
  "stock": 50
}
```
POST /orders
Places an order for selected products.

Example Request:

POST http://localhost:8000/orders
Content-Type: application/json

{
  "products": [
    {
      "product_id": 1,
      "quantity": 2
    },
    {
      "product_id": 2,
      "quantity": 1
    }
  ]
}
Example Response:
```JSON

{
  "id": 1,
  "products": [
    {
      "product_id": 1,
      "quantity": 2
    },
    {
      "product_id": 2,
      "quantity": 1
    }
  ],
  "total_price": 109.97,
  "status": "pending"
}

# DATABASE_URL: Configures the database connection string. Set in the .env file.
