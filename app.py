from werkzeug.security import generate_password_hash, check_password_hash
from website import create_app
import os

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)