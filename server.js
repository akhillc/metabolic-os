const express = require('express');
const { DatabaseSync } = require('node:sqlite');
const path = require('path');
const os = require('os');

const app = express();
const PORT = 3000;

// ── Database setup ──────────────────────────────────────────────────────────

const db = new DatabaseSync(path.join(__dirname, 'metabolic.db'));

db.exec(`
  CREATE TABLE IF NOT EXISTS meals (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    date      TEXT    NOT NULL,
    time      TEXT    NOT NULL,
    description TEXT  NOT NULL,
    net_carbs REAL    DEFAULT 0,
    protein   REAL    DEFAULT 0,
    fat       REAL    DEFAULT 0,
    calories  REAL    DEFAULT 0,
    created_at TEXT   DEFAULT (datetime('now','localtime'))
  );

  CREATE TABLE IF NOT EXISTS inventory (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT NOT NULL,
    category   TEXT NOT NULL DEFAULT 'pantry',
    quantity   TEXT,
    freshness  TEXT NOT NULL DEFAULT 'fresh',
    notes      TEXT,
    added_date TEXT DEFAULT (date('now','localtime'))
  );
`);

// ── Middleware ───────────────────────────────────────────────────────────────

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// ── Helpers ──────────────────────────────────────────────────────────────────

function localDate() {
  const now = new Date();
  return now.toLocaleDateString('en-CA'); // YYYY-MM-DD in local time
}

function localTime() {
  return new Date().toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: true,
  });
}

function sumMacros(meals) {
  return meals.reduce(
    (acc, m) => {
      acc.net_carbs += m.net_carbs || 0;
      acc.protein   += m.protein   || 0;
      acc.fat       += m.fat       || 0;
      acc.calories  += m.calories  || 0;
      return acc;
    },
    { net_carbs: 0, protein: 0, fat: 0, calories: 0 }
  );
}

// ── Meal endpoints ────────────────────────────────────────────────────────────

// POST /api/meals — log a meal
app.post('/api/meals', (req, res) => {
  const { description, net_carbs = 0, protein = 0, fat = 0, calories = 0, date, time } = req.body;

  if (!description) {
    return res.status(400).json({ error: 'description is required' });
  }

  const stmt = db.prepare(`
    INSERT INTO meals (date, time, description, net_carbs, protein, fat, calories)
    VALUES (?, ?, ?, ?, ?, ?, ?)
  `);

  const info = stmt.run(
    date || localDate(),
    time || localTime(),
    description,
    net_carbs,
    protein,
    fat,
    calories
  );

  const meal = db.prepare('SELECT * FROM meals WHERE id = ?').get(Number(info.lastInsertRowid));
  res.status(201).json(meal);
});

// GET /api/meals/today — today's meals + running totals
app.get('/api/meals/today', (req, res) => {
  const today = localDate();
  const meals = db.prepare('SELECT * FROM meals WHERE date = ? ORDER BY id ASC').all(today);
  const totals = sumMacros(meals);

  res.json({
    date: today,
    meals,
    totals,
    budget_remaining: {
      net_carbs: Math.max(0, 50 - totals.net_carbs),
      protein:   Math.max(0, 150 - totals.protein),
    },
    targets: { net_carbs: 50, protein: 150 },
  });
});

// GET /api/meals/history?days=7
app.get('/api/meals/history', (req, res) => {
  const days = parseInt(req.query.days) || 7;
  const rows = db.prepare(`
    SELECT date,
           SUM(net_carbs) AS net_carbs,
           SUM(protein)   AS protein,
           SUM(fat)       AS fat,
           SUM(calories)  AS calories,
           COUNT(*)       AS meal_count
    FROM meals
    WHERE date >= date('now', 'localtime', ? || ' days')
    GROUP BY date
    ORDER BY date DESC
  `).all(`-${days}`);

  res.json({ days, history: rows });
});

// DELETE /api/meals/:id
app.delete('/api/meals/:id', (req, res) => {
  const info = db.prepare('DELETE FROM meals WHERE id = ?').run(req.params.id);
  if (info.changes === 0) return res.status(404).json({ error: 'Not found' });
  res.json({ deleted: true });
});

// ── Inventory endpoints ───────────────────────────────────────────────────────

// GET /api/inventory
app.get('/api/inventory', (req, res) => {
  const items = db.prepare('SELECT * FROM inventory ORDER BY freshness ASC, name ASC').all();
  res.json(items);
});

// POST /api/inventory
app.post('/api/inventory', (req, res) => {
  const { name, category = 'pantry', quantity = '', freshness = 'fresh', notes = '' } = req.body;
  if (!name) return res.status(400).json({ error: 'name is required' });

  const info = db.prepare(`
    INSERT INTO inventory (name, category, quantity, freshness, notes)
    VALUES (?, ?, ?, ?, ?)
  `).run(name, category, quantity, freshness, notes);

  const item = db.prepare('SELECT * FROM inventory WHERE id = ?').get(Number(info.lastInsertRowid));
  res.status(201).json(item);
});

// PATCH /api/inventory/:id — update freshness (or any field)
app.patch('/api/inventory/:id', (req, res) => {
  const { freshness, quantity, notes, category, name } = req.body;
  const item = db.prepare('SELECT * FROM inventory WHERE id = ?').get(req.params.id);
  if (!item) return res.status(404).json({ error: 'Not found' });

  const updated = {
    name:      name      ?? item.name,
    category:  category  ?? item.category,
    quantity:  quantity  ?? item.quantity,
    freshness: freshness ?? item.freshness,
    notes:     notes     ?? item.notes,
  };

  db.prepare(`
    UPDATE inventory
    SET name = ?, category = ?, quantity = ?, freshness = ?, notes = ?
    WHERE id = ?
  `).run(updated.name, updated.category, updated.quantity, updated.freshness, updated.notes, req.params.id);

  res.json(db.prepare('SELECT * FROM inventory WHERE id = ?').get(req.params.id));
});

// DELETE /api/inventory/:id
app.delete('/api/inventory/:id', (req, res) => {
  const info = db.prepare('DELETE FROM inventory WHERE id = ?').run(req.params.id);
  if (info.changes === 0) return res.status(404).json({ error: 'Not found' });
  res.json({ deleted: true });
});

// ── Start server ─────────────────────────────────────────────────────────────

function getLocalIP() {
  const interfaces = os.networkInterfaces();
  for (const iface of Object.values(interfaces)) {
    for (const config of iface) {
      if (config.family === 'IPv4' && !config.internal) {
        return config.address;
      }
    }
  }
  return '127.0.0.1';
}

app.listen(PORT, '0.0.0.0', () => {
  const ip = getLocalIP();
  console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('  🧬 Metabolic OS — Server running');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(`  Local:    http://localhost:${PORT}`);
  console.log(`  iPhone:   http://${ip}:${PORT}   ← bookmark this`);
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
});
