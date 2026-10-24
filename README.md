# QA Automation Portfolio

A Python-based QA automation project demonstrating API and UI testing,
reusable components, test organization, and automated test reporting.

## Test Coverage

### API Testing
- GET requests for valid and invalid user IDs
- API client methods: GET, POST, PUT, PATCH, DELETE
- Request timeout and connection error handling
- Mock-based unit tests for the API client

### UI Testing
- Successful login
- Login with invalid credentials
- Add and remove elements
- Basic page functionality

## Tech Stack

- Python
- pytest
- Requests
- Playwright
- Allure Reports
- python-dotenv
- GitHub Actions

## Setup

Use Python 3.14.7 to match the CI environment.

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies and Chromium:

```bash
python -m pip install -r requirements.txt
python -m playwright install chromium
```

Create a local environment file:

```bash
cp .env.example .env
```

Set the following variable in `.env`:

```text
API_BASE_URL=https://jsonplaceholder.typicode.com
```

## Running Tests

Run the complete test suite:

```bash
python -m pytest
```

Generate fresh Allure results:

```bash
python -m pytest --alluredir=allure-results --clean-alluredir
```

To view the report, install the Allure CLI and run:

```bash
allure serve allure-results
```

## Continuous Integration

GitHub Actions runs the API and UI test suite on pushes and pull requests.
Allure results are uploaded as a workflow artifact for later inspection.
