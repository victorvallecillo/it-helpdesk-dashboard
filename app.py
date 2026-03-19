"""
app.py — IT Helpdesk Dashboard
Author: Victor Vallecillo

A lightweight IT helpdesk ticketing system built with Flask and SQLite.
Features: create/update/close tickets, priority levels, assignment,
dashboard metrics, and filtering.

Usage:
    pip install flask
    python app.py
    Open http://localhost:5000
"""

from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "helpdesk-secret-2024"
DB_PATH = "helpdesk.db"

# ─── Database ────────────────────────────────────────────────────────────────

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS tickets (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT NOT NULL,
            description TEXT NOT NULL,
            category    TEXT NOT NULL DEFAULT 'General',
            priority    TEXT NOT NULL DEFAULT 'Medium',
            status      TEXT NOT NULL DEFAULT 'Open',
            requester   TEXT NOT NULL,
            assigned_to TEXT DEFAULT 'Unassigned',
            created_at  TEXT NOT NULL,
            updated_at  TEXT NOT NULL,
            resolved_at TEXT
        );

        CREATE TABLE IF NOT EXISTS comments (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id  INTEGER NOT NULL,
            author     TEXT NOT NULL,
            body       TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (ticket_id) REFERENCES tickets(id)
        );
        """)

        # Seed sample data if empty
        count = db.execute("SELECT COUNT(*) FROM tickets").fetchone()[0]
        if count == 0:
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            sample_tickets = [
                ("Laptop won't boot after Windows Update", "User reports laptop stuck on spinning circle after last night's update. No BSOD.", "Hardware", "High", "Open", "Alice Johnson", "Victor V.", now, now, None),
                ("Outlook not syncing emails", "Emails not syncing since this morning. Other Office apps working fine.", "Software", "Medium", "In Progress", "Bob Martinez", "Victor V.", now, now, None),
                ("New user onboarding - Sarah Weber", "Create AD account, assign M365 licence, configure laptop, add to Sales group.", "Onboarding", "High", "Open", "HR Dept", "Unassigned", now, now, None),
                ("VPN connection dropping frequently", "VPN drops every 20-30 minutes. Affects 3 users in remote office.", "Network", "High", "In Progress", "Thomas Müller", "Victor V.", now, now, None),
                ("Printer offline in Meeting Room B", "Printer shows offline in Windows. Physical device has no error lights.", "Hardware", "Low", "Open", "Reception", "Unassigned", now, now, None),
                ("Request: Adobe Acrobat licence", "Finance team needs Acrobat Pro for PDF editing. Approval from manager attached.", "Software", "Medium", "Open", "Finance Dept", "Unassigned", now, now, None),
                ("Password reset - locked account", "User locked out after 5 failed attempts. Needs immediate reset.", "Access", "High", "Resolved", "Carlos Ruiz", "Victor V.", now, now, now),
                ("SharePoint permissions not working", "User cannot access the Q1 Reports folder despite being in the correct group.", "Access", "Medium", "Resolved", "Alice Johnson", "Victor V.", now, now, now),
            ]
            db.executemany("""INSERT INTO tickets
                (title, description, category, priority, status, requester, assigned_to, created_at, updated_at, resolved_at)
                VALUES (?,?,?,?,?,?,?,?,?,?)""", sample_tickets)
            db.commit()

# ─── Routes ──────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    db = get_db()
    status_filter  = request.args.get("status", "")
    priority_filter = request.args.get("priority", "")
    category_filter = request.args.get("category", "")
    search = request.args.get("q", "")

    query = "SELECT * FROM tickets WHERE 1=1"
    params = []

    if status_filter:
        query += " AND status = ?"
        params.append(status_filter)
    if priority_filter:
        query += " AND priority = ?"
        params.append(priority_filter)
    if category_filter:
        query += " AND category = ?"
        params.append(category_filter)
    if search:
        query += " AND (title LIKE ? OR requester LIKE ? OR description LIKE ?)"
        params += [f"%{search}%"] * 3

    query += " ORDER BY CASE priority WHEN 'Critical' THEN 1 WHEN 'High' THEN 2 WHEN 'Medium' THEN 3 ELSE 4 END, created_at DESC"
    tickets = db.execute(query, params).fetchall()

    # Metrics
    metrics = {
        "total":       db.execute("SELECT COUNT(*) FROM tickets").fetchone()[0],
        "open":        db.execute("SELECT COUNT(*) FROM tickets WHERE status='Open'").fetchone()[0],
        "in_progress": db.execute("SELECT COUNT(*) FROM tickets WHERE status='In Progress'").fetchone()[0],
        "resolved":    db.execute("SELECT COUNT(*) FROM tickets WHERE status='Resolved'").fetchone()[0],
        "high":        db.execute("SELECT COUNT(*) FROM tickets WHERE priority IN ('High','Critical') AND status!='Resolved'").fetchone()[0],
    }

    categories = [r[0] for r in db.execute("SELECT DISTINCT category FROM tickets").fetchall()]

    return render_template("index.html", tickets=tickets, metrics=metrics,
                           categories=categories, filters={
                               "status": status_filter, "priority": priority_filter,
                               "category": category_filter, "q": search
                           })

@app.route("/ticket/new", methods=["GET", "POST"])
def new_ticket():
    if request.method == "POST":
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        db = get_db()
        db.execute("""INSERT INTO tickets
            (title, description, category, priority, status, requester, assigned_to, created_at, updated_at)
            VALUES (?,?,?,?,?,?,?,?,?)""", (
            request.form["title"],
            request.form["description"],
            request.form["category"],
            request.form["priority"],
            "Open",
            request.form["requester"],
            request.form.get("assigned_to", "Unassigned"),
            now, now
        ))
        db.commit()
        flash("Ticket created successfully.", "success")
        return redirect(url_for("index"))
    return render_template("new_ticket.html")

@app.route("/ticket/<int:ticket_id>")
def view_ticket(ticket_id):
    db = get_db()
    ticket   = db.execute("SELECT * FROM tickets WHERE id=?", (ticket_id,)).fetchone()
    comments = db.execute("SELECT * FROM comments WHERE ticket_id=? ORDER BY created_at", (ticket_id,)).fetchall()
    if not ticket:
        flash("Ticket not found.", "danger")
        return redirect(url_for("index"))
    return render_template("ticket.html", ticket=ticket, comments=comments)

@app.route("/ticket/<int:ticket_id>/update", methods=["POST"])
def update_ticket(ticket_id):
    db  = get_db()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    new_status = request.form.get("status")
    resolved_at = now if new_status == "Resolved" else None

    db.execute("""UPDATE tickets SET
        status=?, priority=?, assigned_to=?, updated_at=?,
        resolved_at=COALESCE(resolved_at, ?)
        WHERE id=?""", (
        new_status,
        request.form.get("priority"),
        request.form.get("assigned_to"),
        now,
        resolved_at,
        ticket_id
    ))
    db.commit()
    flash("Ticket updated.", "success")
    return redirect(url_for("view_ticket", ticket_id=ticket_id))

@app.route("/ticket/<int:ticket_id>/comment", methods=["POST"])
def add_comment(ticket_id):
    db  = get_db()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    db.execute("INSERT INTO comments (ticket_id, author, body, created_at) VALUES (?,?,?,?)",
               (ticket_id, request.form["author"], request.form["body"], now))
    db.execute("UPDATE tickets SET updated_at=? WHERE id=?", (now, ticket_id))
    db.commit()
    return redirect(url_for("view_ticket", ticket_id=ticket_id))

@app.route("/api/metrics")
def api_metrics():
    """JSON endpoint for dashboard stats — useful for future integrations."""
    db = get_db()
    by_status   = {r[0]: r[1] for r in db.execute("SELECT status, COUNT(*) FROM tickets GROUP BY status").fetchall()}
    by_priority = {r[0]: r[1] for r in db.execute("SELECT priority, COUNT(*) FROM tickets GROUP BY priority").fetchall()}
    by_category = {r[0]: r[1] for r in db.execute("SELECT category, COUNT(*) FROM tickets GROUP BY category").fetchall()}
    return jsonify({"by_status": by_status, "by_priority": by_priority, "by_category": by_category})

# ─── Run ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    init_db()
    print("\n  IT Helpdesk Dashboard")
    print("  Running at http://localhost:5000\n")
    app.run(debug=True, port=5000)
