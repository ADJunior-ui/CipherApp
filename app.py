from flask import Flask, render_template, request, jsonify
# Import your original CipherApp engine class from decodeApp.py
from decodeApp import CipherApp

# Initialize the Flask web application server
web_app = Flask(__name__)

# Create a single persistent instance of your core cipher engine
cipher_engine = CipherApp()

@web_app.route('/')
def home():
    """
    Route handler to render the primary dashboard interface.
    """
    # This instructs Flask to look inside your /templates folder for index.html
    return render_template('index.html')

if __name__ == '__main__':
    # Start the local development web server in debug mode
    # Debug mode automatically reloads the page whenever you save changes!
    web_app.run(debug=True)