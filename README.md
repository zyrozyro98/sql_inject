# Local Login Demo (Educational)

This repository contains a small Flask-based demo for learning how login requests can be received and logged in a controlled local environment.

## Important notice

- This project is intended for educational and sandbox use only.
- Use it only against systems you own or have explicit written permission to test.
- Do not use it against third-party or production services without authorization.

## Included

- A local Flask server that exposes a simple `/login` endpoint
- A sample client that can send test form or JSON payloads
- Local capture of received payloads to `captured_creds.txt`

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

## Example credentials file

```json
{
  "credentials": [
    {"username": "admin", "password": "admin123"},
    {"username": "test", "password": "test123"}
  ]
}
```

## Notes

- The local demo is designed to help understand request handling, logging, and payload structure.
- For real-world testing or production deployment, always follow your organization’s security policies and approval procedures.

## Render deployment

If you want to host the demo on Render, create a new web service and use:

- Build Command: `pip install -r requirements.txt`
- Start Command: `python test_login.py`

> For Render, keep this as a lab/demo application only, not as a tool for attacking real systems.
