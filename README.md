# CipherApp Studio 🔒

An elegant, dark-mode cryptography dashboard that bridges a Python cipher engine with a small web UI. The app encodes text into coordinate pairs and decodes coordinate streams back to text, with support for English and Persian scripts.

## Key Features

- Bidirectional encode/decode between text and X,Y coordinates
- Multilingual: English and Persian script handling
- Live vector path visualization (Matplotlib)
- Simple local persistence to `default.txt`

---

## Prerequisites

- Python 3.10 or newer
- Git (optional, for cloning)

## Quick start (Windows)

Open PowerShell or Command Prompt and run the following commands from the project root.

1) (Optional) Create and activate a virtual environment:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1   # PowerShell
# or: venv\Scripts\activate  # cmd.exe
```

2) Install dependencies:

```powershell
pip install -r requirements.txt
```

3) Run the application (development):

```powershell
python app.py
```

4) Open your browser at:

http://127.0.0.1:5000

Notes
- The server runs with Flask's built-in development server. Do not use `debug=True` in production.
- For production deployments, run the app behind a WSGI server (e.g. `gunicorn`) or a Windows-compatible host.

## Usage

- Encode text: switch to "Encode" mode in the UI, enter text and an optional numeric key, then execute.
- Decode coordinates: switch to "Decode" mode and provide coordinates in the format `X,Y X,Y`.

## Project layout

- `app.py` — Flask web server and API
- `decodeApp.py` — `CipherApp` implementation (encoding/decoding, CLI helpers)
- `templates/index.html` — web UI
- `requirements.txt` — Python dependencies

## Contributing & License

- If you want contributors, add a `CONTRIBUTING.md` and a `LICENSE` file.

## Recommended improvements

- Add a small `.env` or config loader for configurable output paths and debug toggles.
- Add unit tests for `CipherApp.encode_message()` and `decode_message()` and a CI workflow.
- Consider documenting the exact cipher mapping used (how characters map to coordinate pairs) for clarity.

If you want, I can apply these improvements directly (README tweaks are done). If you'd like I can also add a `LICENSE` or example `.env` next.