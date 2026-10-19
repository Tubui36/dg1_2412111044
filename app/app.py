import json, os
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)
DATA = os.path.join(os.path.dirname(__file__), "data", "students.json")
MSSV = os.environ.get("MSSV", "2412111044")

def load():
    with open(DATA, encoding="utf-8") as f:
        return json.load(f)

def save(items):
    with open(DATA, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

@app.route("/")
def index():
    return render_template("index.html", students=load(),
                           title="DG1 – Bùi Đình Tú – 2412111044")

@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "student": MSSV})

@app.route("/api/students", methods=["GET"])
def list_students():
    items = load()
    lop = request.args.get("lop")
    if lop:
        items = [s for s in items if s["lop"] == lop]
    return jsonify(items)

@app.route("/api/students/<int:sid>")
def get_student(sid):
    for s in load():
        if s["id"] == sid:
            return jsonify(s)
    return jsonify({"error": "not found"}), 404

@app.route("/api/students", methods=["POST"])
def add_student():
    d = request.get_json(silent=True) or {}
    for k in ("mssv", "ho_ten", "lop", "diem"):
        if k not in d:
            return jsonify({"error": f"thieu truong {k}"}), 400
    if not isinstance(d["diem"], (int, float)) or isinstance(d["diem"], bool) \
       or not 0 <= d["diem"] <= 10:
        return jsonify({"error": "diem phai trong khoang 0-10"}), 400
    items = load()
    new = {"id": max([s["id"] for s in items], default=0) + 1,
           "mssv": d["mssv"], "ho_ten": d["ho_ten"],
           "lop": d["lop"], "diem": d["diem"]}
    items.append(new)
    save(items)
    return jsonify(new), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
