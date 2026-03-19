# 🎫 IT Helpdesk Dashboard

A lightweight, production-inspired IT ticketing system built with Python and Flask. Designed to demonstrate real helpdesk workflow management — creating, assigning, tracking, and resolving IT support tickets.

> **Author:** Victor Vallecillo — IT Support Specialist | Google IT Support Certified | CS50 Harvard  
> **Stack:** Python · Flask · SQLite · HTML/CSS  
> **Live demo:** Run locally in 2 minutes (see below)

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
git clone https://github.com/YOUR_USERNAME/it-helpdesk-dashboard.git
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

| Priority | Response Target | Example |
|---|---|---|
| Critical | Immediate | Server down, data breach |
| High | Same day | Multiple users affected, VPN down |
| Medium | Next business day | Single user issue |
| Low | This week | Cosmetic issue, low-impact request |

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

*Built as part of a hands-on IT portfolio alongside [homelab-infrastructure](https://github.com/YOUR_USERNAME/homelab-infrastructure) and [m365-admin-lab](https://github.com/YOUR_USERNAME/m365-admin-lab).*
