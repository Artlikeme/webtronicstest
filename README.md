
# Test Task for Webtronics
Simple RESTful API using FastAPI for a social networking application




## Environment Variables

To run this project, you will need to add the following environment variables to your .env file in root directory.

DB: 
`DB_HOST` 
`DB_PORT`
`DB_NAME`
`DB_USER`
`DB_PASS`

Secret keys: 
`SECRET_JWT` 
`SECRET_PASS`

API keys: 
`HUNTER_API_KEY` 
`CLEARBIT_KEY`

Api keys from hunter.io and clearbit.com
## Run Locally

Clone the project

```bash
  git clone https://link-to-project
```

Go to the project directory

```bash
  cd my-project
```

Install dependencies

```bash
  python -m venv venv
  source venv/bin/activate
  pip install -r req.txt
```

Start the server

```bash
  uvicorn src.main:app --reload 
```

