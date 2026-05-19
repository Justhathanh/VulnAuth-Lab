from flask import Flask, render_template, request, redirect, url_for, session
from database import get_db
import os

app = Flask(__name__)
app.secret_key = "supersecretkey123"  # VULN: hardcoded weak secret key

def init_db():
    conn = get_db()
    with conn.cursor() as cursor:
        with open("schema.sql", "r") as f:
            for statement in f.read().split(";"):
                stmt = statement.strip()
                if stmt:
                    cursor.execute(stmt)
    conn.commit()
    conn.close()

@app.route("/")
def index():
    return render_template("index.html", user=session.get("user"))

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("auth.login"))
    return render_template("dashboard.html", user=session["user"])

from modules.auth.routes import auth_bp
from modules.session.routes import session_bp

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(session_bp, url_prefix="/session")

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)