# QA Automation Portfolio

A Python-based QA automation framework demonstrating API and UI test automation, reusable testing components, test isolation, mocking, automated reporting, and CI/CD integration.

The project is built with **pytest, Playwright, Requests, Docker, and GitHub Actions**.

## Test Coverage

### API Testing
- GET requests for valid and invalid user IDs
- API client implementation supporting GET, POST, PUT, PATCH, and DELETE
- Request timeout and connection error handling
- Mock-based unit tests for API client behavior
- Test fixtures for creating and cleaning up test resources
- Validation of API response status codes and JSON payloads

### UI Testing
- Successful login and invalid credentials scenarios
- Add and remove elements
- API mocking
- Browser context isolation
- Page Object Model (POM)
- Reusable Playwright fixtures

## Tech Stack

- **Language:** Python 3.14
- **Test Framework:** pytest
- **UI Automation:** Playwright
- **API Testing:** Requests
- **Test Reporting:** Allure Reports
- **Parallel Execution:** pytest-xdist
- **Containerization:** Docker, Docker Compose
- **CI/CD:** GitHub Actions
- **Configuration:** python-dotenv

## Project Structure

```text
qa_automation_portfolio/
├── .github/
│   └── workflows/
│       └── tests.yml
├── client/
│   └── api_client.py
├── pages/
│   └── login_page.py
├── tests/
│   ├── api/
│   │   ├── test_api_client.py
│   │   ├── test_users.py
│   │   └── test_posts.py
│   ├── ui/
│   │   ├── test_login.py
│   │   ├── test_homepage.py
│   │   ├── test_add_remove_elements.py
│   │   ├── test_api_mocking.py
│   │   └── test_context_isolation.py
│   └── test_data/
│       └── login_data.py
├── conftest.py
├── pytest.ini
├── requirements.txt
├── Dockerfile
├── compose.yaml
└── .env.example
```

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

Configure the API base URL in `.env`:

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

View the Allure report (requires Allure CLI):

```bash
allure serve allure-results
```

## Docker

Build and run the test suite using Docker Compose:

```bash
docker compose run --rm tests
```

The Docker image installs Python dependencies and Chromium. API and UI tests run inside a Linux container.

Allure results are saved to the local `allure-results/` directory through a bind mount.

## Continuous Integration

GitHub Actions automatically runs the API and UI test suite on pushes and pull requests targeting the `main` branch.

The workflow includes:

1. Checking out the repository.
2. Setting up Python 3.14.7.
3. Installing project dependencies.
4. Installing Chromium and its system dependencies.
5. Executing the test suite.
6. Uploading Allure test results as workflow artifacts.

After pushes to `main`, a separate job generates an Allure HTML report and publishes it to GitHub Pages. Report history is preserved between deployments.

## Test Environment

The project uses [JSONPlaceholder](https://jsonplaceholder.typicode.com/) as a public demo REST API.

It is intended for practicing API automation and framework design rather than testing a production backend. Some write operations are simulated by the service and do not persist data.
