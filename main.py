# the script to start the app
from project import app

if __name__ == "__main__":
    # normal run
    app.run(debug=True, host="0.0.0.0")