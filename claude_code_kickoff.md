# Metabolic OS — Claude Code Kickoff

## Step 1: Create a project directory

```bash
mkdir -p ~/metabolic-os && cd ~/metabolic-os
```

## Step 2: Copy the PRD into the project

Download `metabolic_os_prd_v1.md` from the Claude chat artifacts and save it to `~/metabolic-os/PRD.md`.

## Step 3: Launch Claude Code with this prompt

Paste this entire block into Claude Code:

---

```
Read PRD.md in this directory. This is a comprehensive product requirements document for a personal metabolic health operating system. You are building Build 1 and Build 2 from the PRD.

## Context

I am non-technical. I rely on you entirely for implementation. I use an iPhone 12 Pro as my primary device and this Mac for development. The system's "brain" is a Claude Project on claude.ai where I have conversations about my health — your job is to build the tools and infrastructure that support that brain.

Persistent storage in Claude artifacts (window.storage) does not work reliably in Projects on mobile. That's why we're building this properly.

## What to build

### Build 1: Metabolic OS Local Server + Dashboard

A lightweight local web app I can access from my iPhone (over local WiFi) that provides:

1. **Daily food log with macro tracking**
   - Log meals with description + macros (net carbs, protein, fat, calories)
   - Running daily totals with progress toward targets: <50g net carbs, 150g+ protein
   - Day resets at midnight
   - Historical data retained (SQLite)

2. **Kitchen inventory**
   - CRUD for items with category (protein, vegetables, dairy, pantry, condiments, snacks) and freshness (fresh, use soon, use today)
   - Persistent across sessions

3. **Dashboard UI**
   - Mobile-first responsive design (iPhone primary)
   - Macro progress rings (carbs = amber, turns red over budget; protein = teal)
   - Today's meal list with timestamps
   - Kitchen inventory panel (collapsible)
   - Med schedule display (static for now):
     - 7pm: Metformin 500mg + Atorvastatin 20mg + Omega-3s 2x690mg
     - 10pm: Magnesium glycinate 350mg + Vitamin D 25mcg
   - Eating window status indicator (fasting before noon, open noon-8pm, closed after 8pm)

4. **REST API**
   - POST /api/meals — log a meal
   - GET /api/meals/today — today's meals + totals
   - GET /api/meals/history?days=7 — historical data
   - DELETE /api/meals/:id — remove a meal
   - GET /api/inventory — list inventory
   - POST /api/inventory — add item
   - DELETE /api/inventory/:id — remove item
   - PATCH /api/inventory/:id — update freshness

### Build 2: Dexcom G7 Data Fetcher

A Python script that pulls CGM data from Dexcom Share API:

1. Install pydexcom
2. Config via .env file (DEXCOM_USERNAME, DEXCOM_PASSWORD)
3. CLI interface:
   - `python cgm.py current` — current glucose + trend arrow
   - `python cgm.py summary --hours 24` — 24hr summary (avg, min, max, time in range)
   - `python cgm.py export --hours 24 --format json` — raw data export
4. Output formatted for easy paste into Claude conversations

## Tech stack preferences

- Backend: Node.js (Express) or Python (Flask) — your call on what's simpler
- Database: SQLite (no external DB setup)
- Frontend: Single HTML file with vanilla JS or lightweight framework — keep it simple
- Python for the Dexcom script (separate from the web app)

## Important constraints

- This runs on my Mac and I access it from my iPhone over local WiFi
- Print the local network URL (like http://192.168.x.x:3000) on startup so I can bookmark it on my phone
- No authentication needed (local network only)
- Dark mode support required (I use dark mode on iPhone)
- No build step — I want to start the server with one command

## After building

1. Test everything works end-to-end
2. Show me the exact commands to start the server
3. Show me the URL to bookmark on my iPhone
4. Run the Dexcom script with a test command and show me the output format

Start by reading the PRD, then build.
```

---

## Step 4: Run the Dexcom script setup

After Claude Code finishes building, you'll need to create a `.env` file with your Dexcom credentials:

```bash
cd ~/metabolic-os
echo "DEXCOM_USERNAME=your_dexcom_email" > .env
echo "DEXCOM_PASSWORD=your_dexcom_password" >> .env
```

## Step 5: Daily usage

Start the server:
```bash
cd ~/metabolic-os && npm start
# or: python app.py
# (Claude Code will tell you the exact command)
```

Open the dashboard URL on your iPhone and bookmark it to your home screen.
