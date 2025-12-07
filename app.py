from flask import Flask, render_template
import sqlite3
import requests

app = Flask(__name__)

def check_tor_connection():
    session = requests.Session()
    session.proxies = {
        'http': 'socks5h://127.0.0.1:9150',
        'https': 'socks5h://127.0.0.1:9150'
    }
    try:
        resp = session.get("http://check.torproject.org", timeout=10)
        if resp.status_code == 200:
            return {"status": "Connected via 9150", "color": "green"}
        else:
            return {"status": "Not Available", "color": "red"}
    except Exception:
        return {"status": "Not Available", "color": "red"}

@app.route("/")
def index():
    conn = sqlite3.connect("crawl_results.db")
    cursor = conn.cursor()
    cursor.execute("SELECT url, status_code, title, content_length, text_snippet, error, timestamp FROM results")
    rows = cursor.fetchall()
    conn.close()

    tor_status = check_tor_connection()
    return render_template("index.html", rows=rows, tor_status=tor_status)

if __name__ == "__main__":
    app.run(debug=True)