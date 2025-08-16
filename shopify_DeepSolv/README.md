# Shopify Insights Fetcher with MySQL (FastAPI)

## Setup

1. Create a MySQL database and user:

```
CREATE DATABASE shopifydb;
```

2. Set your database URL (edit db/database.py):

```
DATABASE_URL = "mysql+pymysql://username:password@localhost:3306/shopifydb"
```

3. Install Python dependencies:

```
pip install -r requirements.txt
```

4. Start the FastAPI server:

```
uvicorn main:app --reload
```

## Usage

POST to `/fetch-shopify-insights` with:
```
{
  "website_url": "https://memy.co.in"
}
```

Response includes brand fetched, and its DB ID.

---

**Note:** This backend is the API layer with MySQL DB. You can use Postman or create a UI to demo.
