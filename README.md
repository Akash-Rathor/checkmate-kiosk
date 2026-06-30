# Kiosk Quest

A simple FastAPI service that accepts an order, calculates the subtotal, discount, total amount, and estimates the preparation time using two prep stations.

## Requirements

* Python 3.10+
* FastAPI
* pytest

## Install

Create a virtual environment and 
```bash
python3 -m venv .venv
```

Activate virtual env
```bash
source ./.venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Run the application

```bash
uvicorn main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Swagger documentation:

```
http://127.0.0.1:8000/docs
```

## API

### POST /order

Example request:

```json
{
  "items": [
    {
      "item_id": 1,
      "qty": 2
    },
    {
      "item_id": 3,
      "qty": 1
    }
  ]
}
```

## Run Tests

```bash
pytest
```
