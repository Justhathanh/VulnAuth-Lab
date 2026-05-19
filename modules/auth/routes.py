from flask import Blueprint, render_template, request, redirect, url_for, session
from database import get_db
auth_bp = Blueprint("auth", __name__)

# VULN 1: SQL Injection + VULN 2: No rate limit (brute-force)
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        conn = get_db()
        try:
            with conn.cursor() as cursor:
                # VULN: string format trực tiếp vào query — SQL Injection
                query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
                cursor.execute(query)
                user = cursor.fetchone()
        except Exception as e:
            error = f"DB Error: {e}"
            return render_template("auth/login.html", error=error)
        finally:
            conn.close()

        if user:
            session["user"] = user["username"]
            session["role"] = user["role"]
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid credentials."

    return render_template("auth/login.html", error=error)


# VULN 3: Plain-text password + VULN 4: User enumeration
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    error = None
    success = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        email    = request.form.get("email", "")

        conn = get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id FROM users WHERE username=%s", (username,))
                existing = cursor.fetchone()

                if existing:
                    # VULN: khác nhau → lộ username tồn tại
                    error = f"Username '{username}' already exists."
                else:
                    # VULN: password lưu plain text
                    cursor.execute(
                        "INSERT INTO users (username, password, email) VALUES (%s,%s,%s)",
                        (username, password, email)
                    )
                    conn.commit()
                    success = "Account created. You can now log in."
        finally:
            conn.close()

    return render_template("auth/register.html", error=error, success=success)


# VULN 5: Predictable reset token + email enumeration
@auth_bp.route("/reset", methods=["GET", "POST"])
def reset():
    message = None
    if request.method == "POST":
        email = request.form.get("email", "")
        conn = get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
                user = cursor.fetchone()
        finally:
            conn.close()

        if user:
            message = f"Reset link: /auth/reset/{user['token']}"
        else:
            # VULN: response khác nhau lộ email tồn tại
            message = "No account found with that email."

    return render_template("auth/reset.html", message=message)


@auth_bp.route("/reset/<token>", methods=["GET", "POST"])
def reset_token(token):
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE token=%s", (token,))
            user = cursor.fetchone()
    finally:
        conn.close()

    if not user:
        return "Invalid token.", 404

    if request.method == "POST":
        new_password = request.form.get("password", "")
        conn = get_db()
        try:
            with conn.cursor() as cursor:
                # VULN: token không bị xóa sau khi dùng
                cursor.execute(
                    "UPDATE users SET password=%s WHERE token=%s",
                    (new_password, token)
                )
                conn.commit()
        finally:
            conn.close()
        return redirect(url_for("auth.login"))

    return render_template("auth/reset_form.html", token=token, username=user["username"])


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))