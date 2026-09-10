# Local Login Demo (Educational)

This repository contains a small Flask-based security testing harness for learning how login requests can be handled and observed in a controlled local environment.

## Important notice

- This project is intended for education, defensive testing, and own-project validation only.
- Use it only against systems you own or have explicit written permission to test.
- Do not use it against third-party or production systems without authorization.

## Included

- A local Flask server that exposes a simple `/login` endpoint
- A test client that can send form or JSON payloads
- Optional capture of received payloads to a file
- Dry-run mode
- JSON report export
- Support for expected status checks

## Requirements

```bash
python -m pip install -r requirements.txt
```

## Run locally

```bash
python test_login.py
```

This will:

1. Start a local demo server on port `5001`
2. Print the local URL for manual testing
3. Run a sample set of requests against the configured target URL

## Example commands

Run against a local endpoint:

```bash
python test_login.py http://localhost:5000/login --no-local-server
```

Send JSON payloads instead of form data:

```bash
python test_login.py http://localhost:5000/login --no-local-server --payload-mode json
```

Use a JSON file with credentials:

```bash
python test_login.py http://localhost:5000/login --no-local-server --credentials-file creds.json
```

Run without sending any real requests (preview only):

```bash
python test_login.py http://localhost:5000/login --no-local-server --dry-run
```

Save a JSON report:

```bash
python test_login.py http://localhost:5000/login --no-local-server --report-file report.json
```

## Example credentials file

```json
{
  "credentials": [
    {"username": "demo_user", "password": "demo_password"},
    {"username": "demo_admin", "password": "demo_admin_password"}
  ]
}
```

## Notes

- The local demo is designed to help understand request handling, logging, and payload structure.
- For real-world testing or production deployment, always follow your organization’s security policies and approval procedures.
- This project intentionally avoids storing sensitive real credentials by default.

## Render deployment

If you want to host the demo on Render, create a new web service and use:

- Build Command: `pip install -r requirements.txt`
- Start Command: `python test_login.py`

> For Render, keep this as a lab/demo application only, not as a tool for attacking real systems.
