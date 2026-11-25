# 🎫 IT Helpdesk Dashboard

A small local ticketing demo built with Python and Flask. It lets you practice common service desk workflows: creating, assigning, updating, and resolving support tickets.

> **Portfolio project:** IT support workflows · Google IT Support Professional Certificate · CS50 Harvard  
> **Stack:** Python · Flask · SQLite · HTML/CSS  
> **Demo:** Run locally with sample tickets (see below)

---

## 📸 Features

- **Dashboard** with live metrics: total tickets, open, in progress, resolved, high-priority count
- **Create tickets** with title, description, category, priority, requester, and assignment
- **Ticket detail view** with status updates, priority changes, reassignment, and threaded comments
- **Filter & search** by status, priority, category, or free-text search
- **Priority-sorted queue** — Critical and High tickets always surface first
- **REST API endpoint** `/api/metrics` returning JSON stats for integration
- **Sample data** pre-loaded on first run — ready to demo immediately

---

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/victorvallecillo/it-helpdesk-dashboard.git
cd it-helpdesk-dashboard

# 2. Install dependency
pip install flask

# 3. Run
python app.py

# 4. Open http://localhost:5000
```

The database is created automatically on first run with sample tickets pre-loaded.

---

## 🗂️ Ticket Categories

| Category | Use Case |
|---|---|
| Hardware | Laptop, printer, peripheral issues |
| Software | App crashes, licence issues, updates |
| Network | VPN, Wi-Fi, connectivity problems |
| Access | Password resets, permission issues, lockouts |
| Onboarding | New user setup — AD, M365, device provisioning |
| Email | Outlook, Exchange, sync issues |

## 🎯 Priority Levels

| Priority | Example target* | Example |
|---|---|---|
| Critical | Immediate | Server down, data breach |
| High | Same day | Multiple users affected, VPN down |
| Medium | Next business day | Single user issue |
| Low | This week | Cosmetic issue, low-impact request |



*These are illustrative targets for the demo, not an SLA. The app does not currently track response timers.*

---

## Practice ticket scenarios

The examples below are fictional exercises for the seeded demo data. They show what a useful ticket can contain; they are not records of real support incidents.

### 1. One user cannot sign in

- **Category / priority:** Access / Medium
- **Capture:** App, device, exact error, time, and whether other services work. Never record a password or MFA code.
- **Work through:** Verify identity, check the account and relevant sign-in record, then follow the approved recovery route.
- **Resolve when:** The user confirms access and the ticket records the checks and outcome.

### 2. New starter is missing Outlook access

- **Category / priority:** Onboarding / Medium
- **Capture:** Start date, manager, requested access, device, and the exact symptom.
- **Work through:** Check the account, intended groups and licence, mailbox availability, and managed-device status where relevant.
- **Resolve when:** The new starter can sign in and open the requested mailbox, or a clear provisioning dependency has been assigned and explained.

### 3. Several users cannot connect to VPN

- **Category / priority:** Network / High
- **Capture:** Number of affected users, location, connection type, start time, and any error message.
- **Work through:** Check whether the issue is shared, record affected scope, provide updates, and escalate to the network owner when needed.
- **Resolve when:** Affected users confirm access is restored and the ticket records the scope, escalation, and verification.

---

## 🔌 API

```bash
# Get ticket stats as JSON
curl http://localhost:5000/api/metrics
```

```json
{
  "by_status":   { "Open": 5, "In Progress": 2, "Resolved": 1 },
  "by_priority": { "High": 3, "Medium": 3, "Low": 2 },
  "by_category": { "Hardware": 2, "Network": 1, "Access": 2, "Software": 2, "Onboarding": 1 }
}
```

---

## 🏗️ Project Structure

```
it-helpdesk-dashboard/
├── app.py                  # Flask app — routes, DB logic, API
├── helpdesk.db             # SQLite database (auto-created)
├── templates/
│   ├── index.html          # Main dashboard
│   ├── ticket.html         # Ticket detail + update + comments
│   └── new_ticket.html     # Create ticket form
└── README.md
```

---

## 💡 Design Decisions

**Why SQLite?** Zero configuration, zero dependencies beyond Flask. The entire database is a single file — easy to reset, inspect, and version-control for demonstration purposes.

**Why no JavaScript framework?** Kept deliberately simple to focus on the IT workflow logic rather than frontend complexity. The UI is clean enough to demo professionally without React overhead.

**Why a REST API endpoint?** Real helpdesk tools expose metrics APIs for integration with monitoring dashboards (Grafana, Power BI). Adding `/api/metrics` demonstrates awareness of real enterprise integration patterns.

---

## 🔮 Possible Extensions

- Email notifications on ticket creation / status change (smtplib)
- SLA timer — flag tickets exceeding response time target
- User authentication (Flask-Login)
- Export tickets to CSV for reporting
- Integration with Microsoft Teams webhook for alerts

---

*Built as part of an IT portfolio alongside [Microsoft 365 Admin Lab](https://github.com/victorvallecillo/m365-admin-lab).*
