from src import app
from flask import render_template

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
