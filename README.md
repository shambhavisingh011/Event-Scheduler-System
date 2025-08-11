
# Event Scheduler System

A simple Flask-based REST API for scheduling, updating, deleting, and searching events. It also supports real-time reminders and keyword search functionality.


## Features

- Create new events
- View all events
- Update or delete an event by ID
- Search events by title or description
- Reminders for upcoming events (within 1 hour)
 - Background thread checks reminders every minute

## Tech Stack

**Language:** Python 3.x

**Framework:** Flask

**API Style:** REST

**Data Storage:** events.json (file-based)

## Installation

Install depenedcies in requirements.txt file
- Python 3.x
- Flask

```bash
  pip install -r requirements.txt
```
    
## Try it with POSTMAN
- Download and install Postman: https://www.postman.com/downloads/
- Start your Flask server:
```bash
   python app.py
```
- Import the provided Postman Collection.
 
🔽 [Download Postman Collection](event_scheduler_collection.json)

- Use the predefined requests to:

   Create a new event

   Get all events

   Update or delete an event

   Search events

   
## POSTMAN Collections Include:
  | Method | URL                                         | Purpose              |
|--------|---------------------------------------------|----------------------|
| GET    | http://127.0.0.1:5000/events                | List all events      |
| POST   | http://127.0.0.1:5000/events                | Create a new event   |
| PUT    | http://127.0.0.1:5000/events/<id>           | Update an event      |
| DELETE | http://127.0.0.1:5000/events/<id>           | Delete an event      |
| GET    | http://127.0.0.1:5000/events/search?q=query | Search events        |

        


## Reminders
The server prints reminders in the terminal for events starting within the next 1 hour. It checks every 60 seconds automatically.

```bash
🔔 Reminder: Event 'Team Meeting' is starting at 2025-06-29T15:00:00
```
## 🔗 Github Linhttps:
https://github.com/shambhavisingh011/Event-Scheduler-System
