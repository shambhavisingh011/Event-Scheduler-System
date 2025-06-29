# Here we are importing necessary libraries
from flask import Flask, request, jsonify  # Flask for API, request to handle incoming data, jsonify to send responses
import json, uuid, os  # json for file operations, uuid to generate unique IDs, os to check file existence
import threading, time  # threading to run reminder checks in background, time to pause between checks(bonus feature)
from datetime import datetime  # datetime to work with date and time
# Here we are creating flask instance
app = Flask(__name__)
# The file "events" is where schedules are stored in json format
DATA_FILE = "events.json"

# Load and save
def load_events():
    if os.path.exists(DATA_FILE):  # Check if the file exists
        with open(DATA_FILE, "r") as f:  # Open file in read mode
            return json.load(f)  # Load and return event data
    return []  # If file doesn't exist, return empty list

# Save the list of events back to the file
def save_events(events):
    with open(DATA_FILE, "w") as f:  # Open file in write mode
        json.dump(events, f, indent=4)  # Save events with nice formatting


# Home route - when user visits http://localhost:5000/
@app.route("/")
def index():
    return "Welcome to the Event Scheduler API!"

# Route to create a new event using POST request
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()  # Read incoming JSON data
    data["id"] = str(uuid.uuid4())  # Generate a unique ID for the event
    events = load_events()  # Load current events
    events.append(data)    # Add new event to the list
    save_events(events)    # Save updated list back to file
    return jsonify(data), 201  # Return the created event and status code 201 (Created)

# Route to get (list) all events
@app.route("/events", methods=["GET"])
def list_events():
    events = load_events()
    if not events:
        return jsonify({"message": "No events found"}), 200  # If empty, it returns a JSON message
    events = sorted(events, key=lambda e: e["start_time"])  # Sort by start time if events exist
    return jsonify(events), 200


# Route to update an existing event by its ID
@app.route("/events/<event_id>", methods=["PUT"])
def update_event(event_id):
    data = request.get_json()  # Get updated event data from request
    events = load_events()    # Load current events
    for i, event in enumerate(events):  # Loop through the events
        if event["id"] == event_id:   # Find event with matching ID
            data["id"] = event_id    # Keep the same ID
            events[i] = data         # Update event data
            save_events(events)       # Save updated list
            return jsonify(data), 200  # Return updated event
    return jsonify({"error": "Event not found"}), 404  # Return error if ID not found
# Route to delete an event by its ID
@app.route("/events/<event_id>", methods=["DELETE"])
def delete_event(event_id):
    events = load_events()  # Load current events
    updated_events = [e for e in events if e["id"] != event_id]  # Filter out the event to delete
    if len(updated_events) == len(events):  # If no event was removed
        return jsonify({"error": "Event not found"}), 404
    save_events(updated_events)  # Save updated list
    return jsonify({"message": "Event deleted"}), 200

# Route to search for events by title or description ( Bonus Feature)
@app.route("/events/search", methods=["GET"])
def search_events():
    query = request.args.get("q", "").lower()  # Get the search query from URL like /events/search?q=meeting
    events = load_events()  # Load current events
    results = [
        event for event in events  # Filter events where query is in title or description
        if query in event["title"].lower() or query in event["description"].lower()
    ]
    if not results:
        return jsonify({"message": "No matching events found"}), 200
    return jsonify(results), 200  # Return matching events

# Function to check for upcoming events and print reminders(Bonus Feature)
def check_reminders():
    while True:
        events = load_events()   # Load all events
        now = datetime.now()     # Get current time
        for event in events:
            start_time = datetime.fromisoformat(event["start_time"])  # Convert string to datetime
            if 0 <= (start_time - now).total_seconds() <= 3600: # Check if it's within the next hour
                print(f"🔔 Reminder: Event '{event['title']}' is starting at {event['start_time']}")
        time.sleep(60)  # check every 60 seconds


if __name__ == "__main__":
    reminder_thread = threading.Thread(target=check_reminders, daemon=True) # Run reminders in background
    reminder_thread.start()
    app.run(debug=True)  # Start the Flask development server
