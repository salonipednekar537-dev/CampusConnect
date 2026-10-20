
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

events = [
    {
        "id": 1,
        "name": "TechFest 2026",
        "category": "Technology",
        "date": "2026-11-15",
        "venue": "Main Auditorium",
        "description": "A day of coding, innovation and technology.",
        "capacity": 100,
        "registrations": 0
    },
    {
        "id": 2,
        "name": "Cultural Night",
        "category": "Cultural",
        "date": "2026-11-20",
        "venue": "College Ground",
        "description": "Celebrate music, dance and college life.",
        "capacity": 150,
        "registrations": 0
    }
]

next_id = 3


@app.route("/")
def home():
    query = request.args.get("q", "").strip().lower()
    category = request.args.get("category", "").strip()

    filtered_events = [
        event for event in events
        if query in event["name"].lower()
        and (not category or event["category"] == category)
    ]

    return render_template(
        "index.html",
        events=filtered_events,
        query=query,
        category=category
    )


@app.route("/add", methods=["POST"])
def add_event():
    global next_id

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

    events.append({
        "id": next_id,
        "name": name,
        "category": category,
        "date": date,
        "venue": venue,
        "description": description,
        "capacity": capacity,
        "registrations": 0
    })

    next_id += 1
    return redirect(url_for("home"))


@app.route("/register/<int:event_id>", methods=["POST"])
def register(event_id):
    event = next(
        (item for item in events if item["id"] == event_id),
        None
    )

    if event is None:
        return "Event not found.", 404

    if event["registrations"] >= event["capacity"]:
        return "This event is full.", 400

    event["registrations"] += 1
    return redirect(url_for("home"))


@app.route("/delete/<int:event_id>", methods=["POST"])
def delete_event(event_id):
    global events

    if not any(event["id"] == event_id for event in events):
        return "Event not found.", 404

    events = [
        event for event in events
        if event["id"] != event_id
    ]

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
