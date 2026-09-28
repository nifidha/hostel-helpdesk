from flask import Flask, request, jsonify, render_template
import sqlite3, random, re

app = Flask(__name__)
DB = "helpdesk.db"

def db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

with db() as c:
    c.execute("""CREATE TABLE IF NOT EXISTS tickets(
        id TEXT PRIMARY KEY, kind TEXT, room TEXT, details TEXT,
        urgency TEXT DEFAULT 'Normal', status TEXT DEFAULT 'Open',
        created TEXT DEFAULT CURRENT_TIMESTAMP)""")

FACILITIES = {
    "mess": "Breakfast 7:30-9, Lunch 12:30-2, Dinner 7:30-9.",
    "wifi": "Wi-Fi is available in all blocks. Get the login from the warden's office.",
    "laundry": "Washing machines are on the ground floor, open 6 AM to 10 PM.",
    "gym": "Gym: 5:30-8:30 AM and 5-9 PM.",
    "visit": "Visitors are allowed 4-6 PM on weekends.",
    "gate": "Gate closes at 9:30 PM.",
}

INTENTS = [  # order matters: first match wins
    ("maintenance", r"repair|fix|leak|fan|light|bulb|broken|not working|plumb"),
    ("complaint",   r"complain|noise|dirty|harass|unclean"),
    ("room",        r"room|allot|allocation|bed|vacat"),
    ("facility",    "|".join(FACILITIES)),
]

def detect(text):
    for name, pattern in INTENTS:
        if re.search(pattern, text.lower()):
            return name
    return "unknown"

@app.route("/")
def index(): return render_template("index.html")

@app.route("/admin")
def admin(): return render_template("admin.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    text = request.json.get("message", "")
    intent = detect(text)
    if intent in ("maintenance", "complaint"):
        return jsonify(action=f"start_{intent}")   # front end runs the question flow
    if intent == "facility":
        key = next(k for k in FACILITIES if k in text.lower())
        return jsonify(reply=FACILITIES[key])
    if intent == "room":
        return jsonify(reply="Rooms are allotted by year and application date. "
                             "For a change, choose 'Room change' and I'll log it.")
    return jsonify(reply="I can help with complaints, repairs, rooms and facilities.")

@app.route("/api/tickets", methods=["POST"])
def create_ticket():
    d = request.json
    tid = "TKT-" + str(random.randint(1000, 9999))
    with db() as c:
        c.execute("INSERT INTO tickets(id,kind,room,details,urgency) VALUES(?,?,?,?,?)",
                  (tid, d["kind"], d["room"], d["details"], d.get("urgency", "Normal")))
    return jsonify(id=tid)

@app.route("/api/tickets", methods=["GET"])
def list_tickets():
    with db() as c:
        rows = c.execute("SELECT * FROM tickets ORDER BY created DESC").fetchall()
    return jsonify([dict(r) for r in rows])

@app.route("/api/tickets/<tid>", methods=["PATCH"])
def update_ticket(tid):
    with db() as c:
        c.execute("UPDATE tickets SET status=? WHERE id=?", (request.json["status"], tid))
    return jsonify(ok=True)

if __name__ == "__main__":
    app.run(debug=True)
