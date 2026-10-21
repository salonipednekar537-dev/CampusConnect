
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DATABASE = "campusconnect.db"


def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                venue TEXT NOT NULL,
                description TEXT DEFAULT '',
                capacity INTEGER NOT NULL CHECK (capacity > 0),
                registrations INTEGER NOT NULL DEFAULT 0
            )
        """)

        count = db.execute(
            "SELECT COUNT(*) FROM events"
        ).fetchone()[0]

        if count == 0:
            db.executemany("""
                INSERT INTO events
                (name, category, date, venue, description, capacity)
                VALUES (?, ?, ?, ?, ?, ?)
            """, [
                ("TechFest 2026", "Technology", "2026-11-15",
                 "Main Auditorium",
                 "A day of coding, innovation and technology.", 100),
                ("Cultural Night", "Cultural", "2026-11-20",
                 "College Ground",
                 "Celebrate music, dance and college life.", 150)
            ])


@app.route("/")
def home():
    query = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()

    sql = "SELECT * FROM events WHERE name LIKE ?"
    params = [f"%{query}%"]

    if category:
        sql += " AND category = ?"
        params.append(category)

    with get_db() as db:
        events = db.execute(
            sql + " ORDER BY date ASC", params
        ).fetchall()

    return render_template(
        "index.html",
        events=events,
        query=query,
        category=category
    )


@app.route("/add", methods=["POST"])
def add_event():
    name = request.form.get("name", "").strip()
    category = request.form.get("category", "").strip()
    date = request.form.get("date", "").strip()
    venue = request.form.get("venue", "").strip()
    description = request.form.get("description", "").strip()
    capacity_text = request.form.get("capacity", "50").strip()

    if not name or not category or not date or not venue:
        return "Please fill in all required fields.", 400

    try:
        capacity = int(capacity_text)
        if capacity < 1:
            raise ValueError
    except ValueError:
        return "Capacity must be a positive number.", 400

    with get_db() as db:
        db.execute("""
            INSERT INTO events
            (name, category, date, venue, description, capacity)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, category, date, venue, description, capacity))

    return redirect(url_for("home"))


@app.route("/register/<int:event_id>", methods=["POST"])
def register(event_id):
    with get_db() as db:
        cursor = db.execute("""
            UPDATE events
            SET registrations = registrations + 1
            WHERE id = ? AND registrations < capacity
        """, (event_id,))

        if cursor.rowcount == 0:
            exists = db.execute(
                "SELECT id FROM events WHERE id = ?", (event_id,)
            ).fetchone()

            if exists is None:
                return "Event not found.", 404

            return "This event is full.", 400

    return redirect(url_for("home"))


@app.route("/delete/<int:event_id>", methods=["POST"])
def delete_event(event_id):
    with get_db() as db:
        cursor = db.execute(
            "DELETE FROM events WHERE id = ?", (event_id,)
        )

        if cursor.rowcount == 0:
            return "Event not found.", 404

    return redirect(url_for("home"))


init_db()

if __name__ == "__main__":
    app.run(debug=True)
