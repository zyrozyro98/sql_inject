"""
⚠️ استخدام تعليمي فقط - لمشروعك الخاص أو بموافقة كتابية
هذا الملف مصمم لاختبار التفاعل مع تطبيقات تسجيل الدخول داخل بيئة محكومة فقط.
"""

import argparse
import json
import threading
import time
from pathlib import Path

import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

# ============================================================
# ⚙️ الإعدادات الافتراضية
# ============================================================
DEFAULT_TARGET_URL = "http://localhost:5000/login"
DEFAULT_LOCAL_PORT = 5001
DEFAULT_CAPTURE_FILE = None

# بيانات تجريبية فقط - استبدلها ببياناتك الخاصة عند الاختبار
DEFAULT_TEST_CREDENTIALS = [
    {"username": "demo_user", "password": "demo_password"},
    {"username": "demo_admin", "password": "demo_admin_password"},
    {"username": "admin", "password": "admin123"},
    {"username": "", "password": ""},
    {"username": "<script>alert(1)</script>", "password": "x"},
]


# ============================================================
# 🖥️ الجزء 1: سيرفر Flask محلي للاختبار
# ============================================================
app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def index():
    """صفحة تسجيل دخول تجريبية بسيطة"""
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
    """يستقبل بيانات تسجيل الدخول ويعرضها فقط إذا تم تمكين الحفظ"""
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

    if DEFAULT_CAPTURE_FILE:
        capture_path = Path(DEFAULT_CAPTURE_FILE)
        capture_path.parent.mkdir(parents=True, exist_ok=True)
        with capture_path.open("a", encoding="utf-8") as file_handle:
            file_handle.write(f"{timestamp}\t{username}\t{password}\n")

    return jsonify({"status": "received", "username": username}), 200


def run_local_server(local_port: int = DEFAULT_LOCAL_PORT, capture_file: str | None = None):
    """تشغيل السيرفر المحلي في الخلفية"""
    print(f"[*] السيرفر المحلي يعمل على http://localhost:{local_port}")
    app.run(host="127.0.0.1", port=local_port, debug=False, use_reloader=False)


# ============================================================
# 📡 الجزء 2: معالجة وسائط سطر الأوامر
# ============================================================
def parse_args():
    """قراءة وسيطات سطر الأوامر"""
    parser = argparse.ArgumentParser(
        description="أداة اختبار تسجيل الدخول على مشروعك الخاص فقط"
    )
    parser.add_argument("target_url", nargs="?", default=DEFAULT_TARGET_URL,
                        help="عنوان URL الخاص بمسار تسجيل الدخول في المشروع")
    parser.add_argument("--local-port", type=int, default=DEFAULT_LOCAL_PORT,
                        help="منفذ السيرفر المحلي عند استخدام السيرفر التجريبي")
    parser.add_argument("--capture-file", default=None,
                        help="مسار ملف اختياري لحفظ البيانات المستلمة. إذا لم تحدده، لن يتم حفظ أي شيء")
    parser.add_argument("--credentials-file", default=None,
                        help="مسار ملف JSON يحتوي على قائمة من بيانات الاعتماد لاختبارها")
    parser.add_argument("--payload-mode", choices=["form", "json"], default="form",
                        help="نمط إرسال بيانات تسجيل الدخول: form أو json")
    parser.add_argument("--delay", type=float, default=0.3,
                        help="الفاصل الزمني بين كل محاولة بالثواني")
    parser.add_argument("--no-local-server", action="store_true",
                        help="عدم تشغيل السيرفر المحلي، فقط اختبار السيرفر الحقيقي")
    parser.add_argument("--keep-alive", action="store_true",
                        help="إبقاء السيرفر المحلي مفتوحًا بعد الانتهاء إن كان قيد التشغيل")
    parser.add_argument("--insecure", action="store_true",
                        help="تجاهل التحقق من شهادة SSL (للاختبار فقط)")
    parser.add_argument("--expect-status", nargs="*", type=int, default=[200, 302],
                        help="رموز HTTP التي تعتبر نجاحًا في الاختبار. مثال: --expect-status 200 302")
    parser.add_argument("--report-file", default=None,
                        help="ملف JSON اختياري لحفظ ملخص النتائج")
    parser.add_argument("--dry-run", action="store_true",
                        help="عدم إرسال الطلبات فعليًا، فقط عرض ما سيتم اختباره")
    return parser.parse_args()


def load_credentials(credentials_file: str | None):
    """تحميل بيانات الاعتماد من ملف JSON أو استخدام القائمة الافتراضية"""
    if not credentials_file:
        return DEFAULT_TEST_CREDENTIALS

    file_path = Path(credentials_file)
    if not file_path.exists():
        raise FileNotFoundError(f"ملف الاعتمادات غير موجود: {credentials_file}")

    raw_data = file_path.read_text(encoding="utf-8")
    data = json.loads(raw_data)

    if isinstance(data, dict) and "credentials" in data:
        data = data["credentials"]

    if not isinstance(data, list):
        raise ValueError("يجب أن يكون ملف الاعتمادات على هيئة قائمة JSON أو كائن يحتوي على credentials")

    normalized = []
    for item in data:
        if isinstance(item, dict) and "username" in item and "password" in item:
            normalized.append({
                "username": str(item["username"]),
                "password": str(item["password"]),
            })

    if not normalized:
        raise ValueError("لم يتم العثور على أي بيانات اعتماد صالحة داخل الملف")

    return normalized


def save_report(report_file: str | None, payload: dict):
    """حفظ ملخص النتائج في ملف JSON إن وُجد"""
    if not report_file:
        return

    report_path = Path(report_file)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def send_to_target(username: str, password: str, url: str, payload_mode: str = "form",
                   verify_ssl: bool = True, dry_run: bool = False):
    """إرسال بيانات تسجيل الدخول إلى السيرفر الهدف"""
    payload = {"username": username, "password": password}
    headers = {"User-Agent": "SecurityTest/1.0"}

    if dry_run:
        print(f"    └─ [dry-run] سيتم إرسال: {payload}")
        return {"status_code": "dry-run", "text": ""}

    try:
        if payload_mode == "json":
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=5,
                allow_redirects=False,
                verify=verify_ssl,
            )
        else:
            response = requests.post(
                url,
                data=payload,
                headers=headers,
                timeout=5,
                allow_redirects=False,
                verify=verify_ssl,
            )

        print(f"    └─ الحالة: {response.status_code} | طول الرد: {len(response.text)} حرف")
        return response

    except requests.exceptions.ConnectionError:
        print(f"    └─ ✗ تعذّر الاتصال بـ {url}")
        return None
    except requests.exceptions.Timeout:
        print(f"    └─ ✗ انتهت المهلة")
        return None


def test_target(url: str, credentials, payload_mode: str = "form", delay: float = 0.3,
                verify_ssl: bool = True, expected_statuses=None, dry_run: bool = False):
    """تشغيل اختبار شامل على السيرفر الهدف"""
    if expected_statuses is None:
        expected_statuses = [200, 302]

    print(f"\n{'='*60}")
    print(f"🎯 الهدف: {url}")
    print(f"{'='*60}")

    results = []
    for cred in credentials:
        print(f"\n[*] تجربة → {cred['username']} : {cred['password']}")
        response = send_to_target(
            cred["username"],
            cred["password"],
            url,
            payload_mode=payload_mode,
            verify_ssl=verify_ssl,
            dry_run=dry_run,
        )

        if response is None:
            results.append({
                "username": cred["username"],
                "password": cred["password"],
                "status": "connection_error",
                "matched_expected": False,
            })
        else:
            status = response.status_code if hasattr(response, "status_code") else response["status_code"]
            matched_expected = status in expected_statuses
            results.append({
                "username": cred["username"],
                "password": cred["password"],
                "status": status,
                "matched_expected": matched_expected,
            })

        if not dry_run:
            time.sleep(delay)

    summary = {
        "target_url": url,
        "payload_mode": payload_mode,
        "expected_statuses": expected_statuses,
        "total": len(credentials),
        "results": results,
        "matched_count": sum(1 for item in results if item.get("matched_expected") is True),
    }

    print(f"\n{'='*60}")
    print(f"📊 ملخص النتائج ({summary['matched_count']}/{len(credentials)} مطابقة للتوقع)")
    print(f"{'='*60}")
    for item in results:
        icon = "✓" if item.get("matched_expected") else "✗"
        print(f"  {icon} {item['username']:20s} → {item['status']}")

    return summary


# ============================================================
# 🚀 نقطة الدخول
# ============================================================
if __name__ == "__main__":
    args = parse_args()
    DEFAULT_CAPTURE_FILE = args.capture_file

    credentials = load_credentials(args.credentials_file)

    print(f"[*] تم تحميل {len(credentials)} بيانات اعتماد للاختبار")

    if args.dry_run:
        print("[*] وضع dry-run مفعل: لن يتم إرسال أي طلب فعلي")

    if not args.no_local_server:
        server_thread = threading.Thread(
            target=run_local_server,
            args=(args.local_port, args.capture_file),
            daemon=True,
        )
        server_thread.start()
        time.sleep(1.5)

        print(f"\n🌐 افتح المتصفح على: http://localhost:{args.local_port}")
        print("   (لتجربة النموذج يدوياً إن أردت)\n")

    summary = test_target(
        args.target_url,
        credentials,
        payload_mode=args.payload_mode,
        delay=args.delay,
        verify_ssl=not args.insecure,
        expected_statuses=args.expect_status,
        dry_run=args.dry_run,
    )

    save_report(args.report_file, summary)

    if args.report_file:
        print(f"\n💾 تم حفظ التقرير في: {args.report_file}")

    if args.no_local_server:
        print("\n[*] تم إنهاء التشغيل بعد إجراء الاختبار على السيرفر الحقيقي.")
        raise SystemExit(0)

    print("\n[*] السيرفر المحلي لا يزال يعمل. اضغط Ctrl+C للإيقاف.")
    if args.keep_alive:
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[!] تم الإيقاف.")
