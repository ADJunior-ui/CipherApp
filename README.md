# CipherApp Studio 🔒

An elegant, dark-mode cryptography dashboard that bridges an advanced Python cipher engine with a reactive web interface. The platform allows users to encode text into coordinate paths or decode coordinate streams back into standard plain text, featuring full operational support for both English and Persian alphabets.

## ⚡ Key Features

- **Bidirectional Cryptography:** Easily encrypt plain text or decrypt structural coordinate pairs.
- **Multilingual Support:** Native processing support for both English alphabets and Persian scripts.
- **Live Vector Tracking:** Generates high-contrast path graphs mapping data coordinate changes dynamically on the fly.
- **State Preservation:** Synchronizes current transaction records automatically into a local `default.txt` backup file.
- **Tailwind CSS Dashboard:** A premium developer console layout styled with clean slate and indigo aesthetics.

---

## 🏃‍♂️ How to Run This Project (Beginner-Friendly Guide)

You do not need to be a programmer to get this application running on your computer. Just follow these simple steps:

### Step 1: Install Python on Your Computer
This app runs on Python. If you don't have it yet:
1. Go to [python.org/downloads](https://www.python.org/downloads/) and download the latest version for your computer (Windows or Mac).
2. Run the installer program you just downloaded.
3. **CRITICAL STEP:** On the very first screen of the installer, look at the bottom and check the box that says **"Add Python to PATH"**. If you skip this, your computer won't understand Python commands.
4. Finish clicking through the installer setup.

### Step 2: Download the Project Files
1. Look at the top right of this GitHub page and click the green **Code** button.
2. Click **Download ZIP** from the dropdown menu.
3. Once downloaded, extract/unzip the file anywhere on your computer (like your Desktop).

### Step 3: Open Your Command Terminal
Your computer has a built-in window for running commands:
- **Windows:** Click your Start Menu, search for **cmd** (Command Prompt), and open it.
- **Mac:** Press `Cmd + Space` to open Spotlight search, type **Terminal**, and open it.

### Step 4: Navigate to the Extracted Folder
You need to tell the terminal to look inside your project folder:
1. Type `cd ` (type cd followed by a single space, do not press enter yet).
2. Find the folder you unzipped in Step 2, click it, and drag-and-drop that folder directly into your terminal window. The terminal will automatically fill in the folder's path location.
3. Press **Enter**.

### Step 5: Install the App's Required Tools
Copy and paste this exact command into your terminal and press **Enter**:
```bash
pip install -r requirements.txt