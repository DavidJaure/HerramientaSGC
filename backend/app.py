from flask import Flask, render_template
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "../frontend")

app = Flask(
    __name__,
    template_folder=os.path.join(FRONTEND_DIR, "templates"),
    static_folder=os.path.join(FRONTEND_DIR, "static")
)

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
