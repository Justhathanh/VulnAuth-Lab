from flask import Blueprint, render_template, request, redirect, url_for, session, make_response
from database import get_db
import time
import hashlib

session_bp = Blueprint("session", __name__)

# VULN 1: Session Fixation
@session_bp.route("/fixation-demo")
def fixation_demo():
    sid = request.args.get("sid")
    if sid:
        # VULN: chấp nhận session ID từ URL — attacker kiểm soát
        session["_id"] = sid
    return render_template("session/fixation.html", sid=sid, current=session.get("_id"))


# VULN 2: Predictable session token
@session_bp.route("/token-gen")
def token_gen():
    # VULN: MD5(timestamp) — predictable trong window 1-2 giây
    raw = str(time.time())
    token = hashlib.md5(raw.encode()).hexdigest()[:16]
    session["gen_token"] = token
    return render_template("session/token_gen.html", token=token, raw=raw)


# VULN 3: No session expiry
@session_bp.route("/no-expiry")
def no_expiry():
    if "user" not in session:
        return redirect(url_for("auth.login"))
    # VULN: không kiểm tra thời gian tạo session
    return render_template("session/no_expiry.html", user=session["user"])


# VULN 4: CSRF — không có token validation
@session_bp.route("/change-email", methods=["GET", "POST"])
def change_email():
    if "user" not in session:
        return redirect(url_for("auth.login"))

    message = None
    if request.method == "POST":
        new_email = request.form.get("email", "")
        # VULN: không kiểm tra CSRF token
        conn = get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE users SET email=%s WHERE username=%s",
                    (new_email, session["user"])
                )
                conn.commit()
        finally:
            conn.close()
        message = f"Email updated to: {new_email}"

    return render_template("session/change_email.html", message=message, user=session["user"])


# VULN 5: Insecure cookie flags
@session_bp.route("/insecure-cookie")
def insecure_cookie():
    resp = make_response(render_template("session/insecure_cookie.html"))
    # VULN: không có HttpOnly, Secure, SameSite
    resp.set_cookie("auth_token", "user_session_abc123",
                    httponly=False,
                    secure=False,
                    samesite=None)
    return resp