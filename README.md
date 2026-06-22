# CipherApp Studio 🔒

A simple Flask project that lets you turn text into coordinate pairs and turn those pairs back into text.

## What it does

- Encode text into coordinate values
- Decode coordinate values back into text
- Show a small graph of the points
- Save the latest result to `default.txt`

## How to run

1. Install Python 3.10+
2. Open the project folder in a terminal
3. Create a virtual environment

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

4. Install the needed packages

```powershell
pip install -r requirements.txt
```

5. Start the app

```powershell
python app.py
```

6. Open this in your browser:

```text
http://127.0.0.1:5000
```

## How to use

- Use **Encode** mode to turn text into coordinates.
- Use **Decode** mode to enter coordinates like `5,3 2,7`.

## Testing

Run the full test suite with:

```powershell
python -m unittest discover -s tests -v
```

The test suite covers:
- Cipher logic (encoding, decoding, validation)
- Flask routes and error handling
- Edge cases and input validation

## File overview

- `app.py` — Flask web app and request handling
- `decodeApp.py` — simple cipher logic
- `templates/index.html` — the UI
- `requirements.txt` — package list
- `tests/` — unit tests for the app

## Note

This is a fun learning project, not a real secure encryption tool.
