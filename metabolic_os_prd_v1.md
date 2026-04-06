# Metabolic Operating System — Product Requirements Document

**Version:** 1.0 (Draft)
**Date:** April 4, 2026
**Author:** Akhill + Claude
**Status:** Discovery → Active Spec

---

## 1. Vision & Problem Statement

### The Problem
Health behavior change fails because tracking systems are passive — they collect data but don't make decisions. The user is left to interpret dashboards, remember goals, and make real-time food/exercise/med choices unassisted. The feedback loop is too slow (weekly weigh-ins, quarterly labs) and the friction of logging is too high.

### The Vision
A **personal metabolic operating system** with Claude as the active decision-making brain, sensors as inputs, and daily choices as outputs. The system should make the right choice the easy choice, every single time — across meals, meds, exercise, and sleep.

### The User
- Male, mid-career, family (wife + 2 kids ages 10 and 6)
- Diagnosed: elevated LDL, insulin resistance indicators
- Medications: atorvastatin 20mg, metformin 500mg ER (ramping to 1000mg)
- Supplements: omega-3s, magnesium glycinate, vitamin D
- Temporary eye medications (short-term, April 2026)
- Cooks for family — meals must work for everyone
- iPhone 12 Pro (planning upgrade), considering Apple Watch SE
- Active Dexcom G7 CGM
- Cronometer free tier (not yet Gold)
- Technical orientation: design thinker, not a coder — relies on Claude Code for builds
- Current weight: 193 lbs
- Daily targets: <50g net carbs, 150g+ protein, noon–8pm eating window

---

## 2. Competitive Landscape

### The Market: AI + CGM + Personalized Nutrition

The space is crowded. At least 25 AI-powered nutrition apps exist as of 2026, using computer vision, NLP, and machine learning for meal plans, real-time tracking, and behavioral coaching. The most relevant competitors:

| Product | What It Does | CGM? | AI Type | Pricing |
|---|---|---|---|---|
| **January AI** | Glucose prediction, photo food logging, AI nutritionist ("Jan"), macro tracking, blood test interpretation | Yes (optional) | Purpose-built ML models + generative AI | Subscription |
| **Signos** | Real-time glucose feedback, exercise suggestions based on spike patterns, weight management | Yes (required) | Proprietary algorithm | ~$200-400/mo (incl. CGM) |
| **Levels Health** | Metabolic scoring per meal, CGM data visualization, behavioral insights | Yes (required) | Proprietary scoring | Subscription + CGM cost |
| **Nutrisense** | CGM data + 1:1 dietitian coaching, food logging | Yes (required) | Human dietitian + basic AI | ~$200-350/mo |
| **Zoe** | Blood/gut microbiome testing → personalized food scores | No (blood test) | ML on biomarker data | ~$60/mo after test kit |
| **Noom** | Behavioral psychology coaching, calorie tracking, habit formation | No | Rule-based + some ML | ~$50-70/mo |
| **Cronometer** | Deep micronutrient tracking (84 nutrients), food database, macro/micro analysis | No (imports health data) | Minimal AI | Free / $5/mo Gold |

### What They All Get Wrong (For This Use Case)

**1. Single-user, single-domain.** Every product above is designed for one person optimizing one thing (glucose, weight, nutrition). None of them plan a family dinner where dad eats sub-50g carbs while the kids eat normally. None of them cross-reference your medication schedule with your meal timing. None of them program your resistance training AND adjust your carb budget on rest days vs. training days. They're point solutions in a system-level problem.

**2. Shallow memory.** January AI's "Jan" remembers your consultation. But it doesn't know your mushrooms are getting old, that berberine conflicts with your metformin, that you have a Peloton and rowing machine in your building gym, or that your 6-year-old won't eat mushrooms. The depth of persistent context in a Claude Project is orders of magnitude richer than any purpose-built health app.

**3. Locked ecosystems.** With Signos or January, you're locked into their algorithm, their food database, their UI, their business model. If they pivot, get acquired, raise prices, or shut down, your data and your system die with them. A Claude Project running on a general-purpose AI platform is portable, extensible, and gets smarter every model generation without migration.

**4. Form-based UX.** Every app in this space makes you tap through UI flows — select a meal, pick portions, confirm macros, tap save. The conversational interface ("I just had 3 eggs with avocado and some of those TJ chickpeas, maybe a quarter can") is fundamentally lower friction. Natural language is the original human interface.

**5. No proactive intelligence.** These apps wait for you to open them. They don't notice that you haven't logged lunch, that your glucose is trending high this week compared to last, or that you're about to hit your 4-week metformin tolerance checkpoint. They track. They don't think.

### What This System Does Differently

| Capability | Typical Health App | This System (Metabolic OS) |
|---|---|---|
| Memory depth | Preferences + food log | Full life context: family, meds, recipes, goals, contraindications, kitchen inventory, conversation history |
| Decision scope | Single domain (food OR exercise OR glucose) | Cross-domain: food × exercise × meds × sleep × family × CGM, all integrated |
| Family awareness | None | Plans one meal with personal low-carb variant + family-friendly base |
| Medication integration | Basic pill reminder | Interaction checking, dose ramp tracking, timing optimization relative to meals |
| Adaptability | Fixed algorithm updates | General-purpose AI that improves every model generation; infinitely extensible via conversation |
| UX model | Form-based logging | Conversational — natural language in, structured advice out |
| Proactive intelligence | Passive (waits for user) | Active — checks for gaps, nudges, flags patterns, asks about missed check-ins |
| Data ownership | Vendor-locked | User-owned context in Claude Project; portable recipes, goals, and protocols |
| Cost structure | $50-400/mo subscriptions | Claude Pro ($20/mo) + sensors (CGM, Watch) — no health-app subscription tax |

### Strategic Positioning

This is not a product to sell. It is a **personal operating system** — a bespoke configuration of general-purpose AI + sensors + behavioral protocols designed for one user's exact needs. The competitive advantage isn't a novel algorithm (it's not); it's the **depth of personalization** that emerges from hundreds of conversations with a context-aware AI that remembers everything.

The closest analogy isn't another health app — it's having a personal concierge doctor, nutritionist, and coach who shares a brain, knows your family, and is available 24/7 for $20/month.

**Future opportunity (not current scope):** The *pattern* — "Claude Project as personal health brain with sensor integrations" — could become a template other people replicate. The platform layer belongs to Anthropic. The system design and protocol knowledge captured in this PRD is the reusable intellectual contribution.

---

## 3. Design Principles

### Principle 1: Active Intelligence, Not Passive Tracking
The system doesn't just record what happened — it advises what to do next. Every interaction should end with a clear recommendation or action.

### Principle 2: Conversation Is the Interface
The primary UX is talking to Claude. Dashboards and tools exist to support the conversation, not replace it. The system should feel like talking to a knowledgeable health advisor who knows your full history, not like filling out forms.

### Principle 3: Family-Compatible by Default
Every meal recommendation must work for the whole family. The system produces ONE meal plan with a low-carb personal variant, not a separate "diet meal" for the user.

### Principle 4: Durable Over Aggressive
Prefer sustainable habits over extreme interventions. The system should be calibrated to produce behavior change that lasts years, not weeks.

### Principle 5: Progressive Enhancement
Start with conversation-only (Phase 0). Layer in tools, sensors, and automations incrementally. Each addition should demonstrably reduce friction or improve outcomes. If it doesn't, skip it.

---

## 4. System Architecture

### Pattern: Hub-and-Spoke

```
┌─────────────────────────────────────────────┐
│              SENSOR LAYER                    │
│  Cronometer · Dexcom G7 · Apple Watch · Cam │
└──────────────────┬──────────────────────────┘
                   │ data flows in
                   ▼
┌─────────────────────────────────────────────┐
│         CLAUDE PROJECT — THE HUB            │
│                                             │
│  Memory: goals, meds, history, preferences  │
│  Project files: recipe library              │
│  Persistent storage: daily log, inventory   │
│  Tools: MCP servers (future)                │
│                                             │
└──────────────────┬──────────────────────────┘
                   │ decisions flow out
                   ▼
┌─────────────────────────────────────────────┐
│             OUTPUT LAYER                     │
│  Meal advice · Macro dashboard · Med nudges │
│  Weekly reviews · Grocery lists · Meal plans│
└──────────────────┬──────────────────────────┘
                   │ outcomes feed back
                   ▼
┌─────────────────────────────────────────────┐
│            FEEDBACK LAYER                    │
│  CGM patterns · Lab results · Weight trend  │
│  Quarterly recalibration                    │
└─────────────────────────────────────────────┘
```

### Why Hub-and-Spoke (Not Multi-Agent)
Separate agents can't share state. The meal advisor needs to know what the exercise coach programmed, and neither can work without the med schedule. A single Claude Project with specialized tools avoids the state-sharing problem entirely.

**Future evolution:** As Claude's platform adds inter-project communication or true agent orchestration, the hub can delegate to specialized sub-agents. The PRDs below are written to enable that separation when the time comes.

### Technical Stack
| Component | Technology | Status |
|---|---|---|
| Brain | Claude Project (this one) | Active |
| Daily state persistence | Artifact persistent storage (`window.storage`) | To build |
| Macro dashboard | React artifact with persistent storage | To build |
| Kitchen inventory | Persistent storage + conversational CRUD | To build |
| Dexcom G7 data | Python script via pydexcom (unofficial) or Dexcom API | To build |
| Nudge system | iOS Reminders (native) + deep links | Partially active |
| Recipe database | Project files (PDFs) + persistent storage | Partially active |
| Cronometer sync | Manual for now; MCP server (future) | Manual |
| Apple Watch data | Apple Health → Cronometer → manual (future: MCP) | Not started |

---

## 5. Agent 1: Meal Advisor — Detailed PRD

### 5.1 Problem Statement
The user makes 3-5 food decisions per day. Each decision needs to account for: daily carb budget remaining, what's already been eaten, what's available in the kitchen, family meal compatibility, and metabolic goals. Currently, this requires starting a new conversation and re-stating context each time.

### 5.2 User Stories

**US-1: "What should I eat right now?"**
As a user at mealtime, I want to ask Claude what to eat and get a recommendation that accounts for everything I've already eaten today, what's in my kitchen, and my remaining carb budget — without re-explaining any of that context.

**US-2: "Here's what I ate — log it"**
As a user who just finished eating, I want to tell Claude what I had (in natural language) and have it logged with accurate macro estimates, updating my daily running total automatically — persisting across conversations.

**US-3: "What's my macro picture today?"**
As a user between meals, I want to glance at a dashboard showing my carb/protein/fat totals for today, my remaining budget, and how many meals I have left in my eating window — without starting a conversation.

**US-4: "Update my kitchen inventory"**
As a user who just went grocery shopping, I want to tell Claude what I bought and have my kitchen inventory updated, so future meal recommendations reflect what's actually available.

**US-5: "Plan dinner for the family tonight"**
As a user planning dinner, I want a recommendation that works for my wife and kids (who eat carbs normally) AND fits my sub-50g daily carb target — one meal, two variants.

**US-6: "I just got a rotisserie chicken — what do I do with it?"**
As a user with a specific ingredient, I want Claude to build a complete meal around it using what's in my kitchen, with macro breakdown and family-friendly plating.

### 5.3 Core Capabilities

#### 4.3.1 Daily Food Log (Persistent)
- Stores meals logged today with timestamps, descriptions, and estimated macros
- Running totals: net carbs, protein, fat, calories
- Remaining budget calculation (50g carbs - consumed = remaining)
- Persists across multiple conversations in the same day
- Resets at midnight (or user-defined day boundary)
- Historical data retained for weekly/monthly analysis

#### 4.3.2 Kitchen Inventory (Persistent)
- Categories: proteins, vegetables, dairy, pantry staples, condiments, snacks
- Each item: name, approximate quantity, expiration status (fresh/getting old/use soon)
- CRUD via natural language: "I bought broccoli, chicken thighs, and cheddar"
- Depletion suggestions: "Your mushrooms are getting old — use tonight"
- Grocery list generation based on planned meals vs. current inventory

#### 4.3.3 Meal Recommendation Engine
- Input: time of day, carb budget remaining, kitchen inventory, family constraints
- Output: specific meal recommendation with:
  - What to make (with instructions or recipe reference)
  - Macro breakdown (net carbs, protein, fat, calories)
  - Family variant (what the kids/wife eat alongside)
  - Prep time estimate
  - Post-meal walk reminder
- Should reference the recipe library (project files) when applicable
- Should suggest new recipes that fit the profile

#### 4.3.4 Macro Dashboard (Visual Artifact)
- React artifact with persistent storage
- Displays:
  - Today's date and eating window status (fasting / eating / window closed)
  - Carb budget: used / remaining (progress bar, color-coded)
  - Protein target: current / goal
  - Fat: current (no hard cap, but tracked)
  - Calories: current / estimated
  - Meals logged today (list with timestamps)
  - Kitchen inventory summary (collapsible)
  - Quick action buttons:
    - "Log a meal" → sendPrompt('I just ate: ')
    - "What should I eat?" → sendPrompt('Based on my macro budget and kitchen inventory, what should I eat right now?')
    - "Update inventory" → sendPrompt('Update my kitchen inventory: ')
    - "Show CGM data" → sendPrompt('Show my latest Dexcom G7 glucose data')

### 5.4 Data Schema

#### Daily Food Log Entry
```json
{
  "date": "2026-04-04",
  "meals": [
    {
      "id": "meal_001",
      "time": "12:15",
      "description": "3 eggs fried in olive oil, avocado, mixed greens, TJ chickpeas (1/4 can), lemon, olive oil drizzle",
      "macros": {
        "net_carbs_g": 14,
        "protein_g": 28,
        "fat_g": 35,
        "calories": 480
      },
      "source": "manual_log",
      "recipe_ref": "mediterranean_egg_chickpea_salad"
    }
  ],
  "totals": {
    "net_carbs_g": 14,
    "protein_g": 28,
    "fat_g": 35,
    "calories": 480
  },
  "budget_remaining": {
    "net_carbs_g": 36,
    "protein_g": 122
  }
}
```

#### Kitchen Inventory Item
```json
{
  "name": "baby bella mushrooms",
  "category": "vegetables",
  "quantity": "1 package (8oz)",
  "freshness": "use_soon",
  "added_date": "2026-04-02",
  "notes": "getting old per user"
}
```

### 5.5 Technical Implementation

#### What Claude Code Builds:

**Build 1: Macro Dashboard Artifact (React + Persistent Storage)**
- File: `macro_dashboard.jsx` or `macro_dashboard.html`
- Uses `window.storage` API for persistence
- Storage keys:
  - `food-log:{date}` — daily food log (JSON)
  - `kitchen-inventory` — current inventory (JSON)
  - `daily-targets` — carb/protein/fat/cal targets (JSON)
- UI: progress bars, meal list, inventory panel, action buttons
- Responsive for mobile (iPhone primary)
- Dark mode support required
- Action buttons use `sendPrompt()` to trigger Claude conversations

**Build 2: Dexcom G7 Data Fetcher (Python Script)**
- Uses pydexcom library (unofficial) or Dexcom Share API
- Fetches: current glucose, 24hr trend, time-in-range stats
- Output: formatted summary Claude can interpret
- Delivery mechanism: TBD (see §6 below)
- Frequency: on-demand or scheduled

**Build 3: iOS Shortcuts (future)**
- "Log Meal" shortcut: opens Claude app with pre-filled prompt
- "Quick Check" shortcut: opens macro dashboard artifact
- "Grocery Run" shortcut: triggers inventory + meal plan conversation

### 5.6 Success Metrics
| Metric | Target | Timeframe |
|---|---|---|
| Daily food logging consistency | >5 days/week | Weeks 1-4 |
| Average daily net carbs | <50g | Weeks 2-8 |
| Meal advisor usage | >2 interactions/day | Weeks 1-4 |
| Kitchen inventory freshness | Updated weekly | Ongoing |
| User-reported friction | "Easy" or "very easy" | Week 4 check-in |

---

## 6. Dexcom G7 Integration — PRD

### 6.1 Problem Statement
CGM data is trapped in the Dexcom app. To get glucose insights into Claude's decision-making (e.g., "your glucose spiked 40 points after rice last time — skip it tonight"), the data needs to flow programmatically.

### 6.2 Technical Options

#### Option A: pydexcom (Unofficial Python Library)
- Uses Dexcom Share/Follow API (same as Dexcom Follow app)
- Requires: Dexcom account credentials, Share feature enabled
- Returns: current glucose, trend arrow, 24hr history
- Limitations: unofficial, could break; no long-term historical data
- Effort: Low (few hours to build)

#### Option B: Dexcom Developer API (Official)
- Requires: developer account, OAuth2 flow, partner approval for production
- Returns: full CGM data (EGVs, calibrations, events)
- Limitations: approval process, more complex auth
- Effort: Medium-high

#### Option C: Manual Screenshots
- User shares Dexcom app screenshots with Claude
- Claude interprets the chart visually
- Limitations: no structured data, manual effort
- Effort: Zero (already works)

### 6.3 Recommended Approach
**Start with Option C (screenshots) immediately.** Build Option A (pydexcom) as a CLI script the user can run on-demand. Revisit Option B only if pydexcom breaks or official API access becomes easier.

### 6.4 Data Flow (Option A)
```
Dexcom G7 sensor
    → Dexcom app (iPhone)
    → Dexcom Share cloud
    → pydexcom script (local or hosted)
    → formatted JSON
    → paste into Claude conversation OR future MCP server
```

### 6.5 What Claude Code Builds
- Python script using pydexcom
- CLI interface: `python fetch_cgm.py --hours 24 --format summary`
- Output formats: summary (for pasting to Claude), JSON (for dashboard), chart data
- Config: credentials stored in `.env` file (never committed)
- [DECISION NEEDED]: Where does this script run? User's Mac? A simple cloud function? This affects how data reaches Claude on mobile.

---

## 7. Nudge System — PRD

### 7.1 Problem Statement
Claude cannot push-notify the user. The user must initiate every conversation. Without external triggers, the system depends entirely on the user remembering to check in — which is the exact habit formation problem we're trying to solve.

### 7.2 Current State
Three iPhone reminders set:
- 12:00 PM — "Break-fast check-in: tell Claude what you're eating"
- 7:00 PM — "Dinner check-in + meds taken?"
- 10:00 PM — "Day close: exercise, meds, sleep time → Claude"

### 7.3 Design Requirements

#### 6.3.1 Nudge Timing
| Nudge | Time | Purpose | Trigger |
|---|---|---|---|
| Break-fast | 12:00 PM | First meal planning | iOS Reminder |
| Afternoon | ~3:00 PM | Mid-day check-in, snack planning | iOS Reminder |
| Dinner | 7:00 PM | Dinner planning + med reminder | iOS Reminder |
| Day close | 10:00 PM | Log exercise, confirm meds, sleep | iOS Reminder |
| Post-meal walk | Dynamic | Remind to walk after logging a meal | [TBD] |

#### 6.3.2 Nudge Content
Each reminder should include a specific, actionable prompt — not just "check in with Claude." Examples:
- "Break-fast: open Claude → 'What should I eat for my first meal?'"
- "Dinner: open Claude → 'Plan dinner with what's in my kitchen. Meds taken: yes/no'"
- "Day close: open Claude → 'Day close. Exercise: [X]. Meds: [taken/missed]. Bed by: [time]'"

#### 6.3.3 [OPEN QUESTION: Escalation]
What happens when the user misses a nudge? Options:
- Nothing (passive — current state)
- A follow-up reminder 30 min later
- The next conversation with Claude opens with "I notice you missed your noon check-in — what did you eat?"

#### 6.3.4 [OPEN QUESTION: Post-Meal Walk Trigger]
The post-meal walk is "non-negotiable" in the protocol. How to trigger it?
- Manual: Claude reminds the user at the end of every meal log conversation
- Automated: iOS Shortcut that fires 5 min after a meal is logged
- Apple Watch: haptic tap reminder (requires Watch)

### 7.4 What Claude Code Builds
- iOS Shortcuts that:
  - Deep-link to Claude app with pre-filled prompts
  - Can be triggered by Reminders or Shortcuts automations
- Reminder creation via Claude's reminder tools (already available)
- [FUTURE]: Apple Watch complication showing macro budget remaining

---

## 8. Future Agents (Stubs — To Be Specced)

These are the remaining agents in the system. Each will get a full PRD once the Meal Advisor is stable and validated.

### 8.1 Exercise Coach
- Programs resistance training (3x/week) using building gym equipment (Peloton, rowing machine, free weights)
- Tracks Zone 2 cardio sessions
- Adjusts programming based on recovery, schedule, and goals
- Integrates with Apple Watch activity data (future)

### 8.2 Med & Supplement Tracker
- Daily adherence tracking for: atorvastatin, metformin, omega-3s, magnesium, vitamin D
- Temporary med tracking (eye medications — time-limited)
- Interaction checking (berberine + metformin contraindication already flagged)
- Dose adjustment tracking (metformin 500mg → 1000mg at 4-week mark)
- Grapefruit avoidance reminder (atorvastatin interaction)

### 8.3 Menu Scanner
- Photo of restaurant menu → structured analysis
- Recommends best options based on macro budget and daily intake
- Flags hidden carbs, sauces, preparation methods
- Lower priority given user mostly cooks at home

### 8.4 Weekly Analyst
- Sunday evening review ritual
- Aggregates: daily macro averages, exercise frequency, med adherence, sleep patterns
- Compares against targets
- Identifies patterns (e.g., "carbs creep up on weekends")
- Adjusts coming week's plan
- Prepares talking points for PCP visits

### 8.5 Family Meal Planner
- Weekly meal plan generation
- Constraints: user's low-carb targets + family-friendly meals
- Grocery list output
- Recipe rotation to avoid monotony
- Uses recipe library + discovers new recipes fitting the profile

---

## 9. Phased Build Roadmap

### Phase 1: Foundation (This Week)
- [x] Claude Project as hub (active)
- [ ] Daily nudge reminders (3 set, add 4th at 3pm)
- [x] Dexcom G7 active
- [x] **BUILD: Macro Dashboard artifact** with persistent storage
- [ ] **BUILD: Kitchen inventory** in persistent storage
- [ ] Establish daily logging habit via conversation

### Phase 2: Data Layer (Week 2-3)
- [x] **BUILD: Dexcom G7 data fetcher** (pydexcom script) -- pydexcom doesn't support G7, use screenshot workflow...
- [ ] Validate Cronometer free tier workflow
- [ ] Decide on Cronometer Gold upgrade based on logging friction
- [ ] **BUILD: Enhanced nudge system** with iOS Shortcuts + deep links
- [ ] Load all project file recipes into persistent storage with macro data

### Phase 3: Intelligence (Week 4-6)
- [ ] **BUILD: Meal recommendation engine** logic in Claude Project system prompt
- [ ] CGM data correlation: which meals spike glucose?
- [ ] First weekly review ritual
- [ ] Metformin dose increase assessment (4-week mark)
- [ ] Follow-up labs preparation

### Phase 4: Hardware & Expansion (Week 6-12)
- [ ] Apple Watch SE acquisition + setup
- [ ] Sleep and exercise data flowing into system
- [ ] Exercise Coach agent PRD + build
- [ ] Med Tracker agent PRD + build
- [ ] Family Meal Planner agent PRD + build

### Phase 5: Optimization (Ongoing)
- [ ] Quarterly CGM re-check sprints
- [ ] Lab result integration and goal adjustment
- [ ] System performance review (is this actually working?)
- [ ] Evaluate multi-agent separation when platform supports it

---

## 10. Open Questions & Decisions Needed

| # | Question | Options | Decision |
|---|---|---|---|
| 1 | Where does the pydexcom script run? | User's Mac (local CLI) | **DECIDED** |
| 2 | Nudge escalation on missed check-ins? | Claude checks time + log gaps at conversation start | **DECIDED** |
| 3 | Post-meal walk trigger mechanism? | Claude verbal reminder at end of every meal log | **DECIDED** |
| 4 | Cronometer Gold upgrade timing? | Now / after 2-week free trial / skip | TBD |
| 5 | Day boundary for food log reset? | Midnight / first meal / custom time | TBD |
| 6 | iPhone upgrade timing? | Now / with Apple Watch / not urgent | TBD |
| 7 | Macro targets — refine protein/fat? | 150g protein/day minimum (0.8g/lb at 193 lbs) | **DECIDED** |
| 8 | Calorie target? | Let macros drive it (no explicit cal target for now) | **DECIDED** |

---

## Appendix A: Recipe Library (Current)

| Recipe | Source | Net Carbs/Serving | Low-Carb Notes |
|---|---|---|---|
| Turkey Burgers | Downshiftology | ~1g/patty | Lettuce wrap or burger bowl |
| Chicken Tacos | Once Upon a Chef | ~26g with shells | Skip shells for ~8g |
| Turkey Bolognese | Ina Garten / Emily Blunt | ~74g with pasta | Needs zucchini noodle or cauliflower rice swap |
| Mediterranean Egg & Chickpea Salad | Custom (built in this project) | ~12g | Limit chickpeas to 1/4 can |

## Appendix B: Medication Schedule

| Time | Medication | Dose | Notes |
|---|---|---|---|
| 7:00 PM (dinner) | Metformin ER | 500mg (→1000mg at week 4) | Take with food |
| 7:00 PM (dinner) | Atorvastatin | 20mg | Evening preferred |
| 7:00 PM (dinner) | Omega-3 fish oil | 2 × 690mg | With food |
| 10:00 PM (bedtime) | Magnesium glycinate | 350mg | Supports sleep |
| 10:00 PM (bedtime) | Vitamin D | 25mcg | — |

### Temporary Eye Medications (through April 6, 2026)
| Medication | Dose | Frequency |
|---|---|---|
| Valacyclovir HCL 500mg | 2 tablets orally | 3x/day |
| Moxifloxacin 0.5% drops | 1 drop left eye | 4x/day |
| Timolol maleate 0.5% drops | 1 drop each eye | 2x/day |
| Latanoprost 0.005% drops | 1 drop each eye | At bedtime |
| Erythromycin 0.5% ointment | Left eye | 2x/day |

## Appendix C: Contraindications & Interactions
- **Berberine + Metformin**: Do NOT combine without explicit PCP approval. Overlapping AMPK activation mechanisms; risk of hypoglycemia and GI issues.
- **Grapefruit + Atorvastatin**: Avoid entirely. Grapefruit inhibits CYP3A4, increasing statin blood levels and side effect risk.
- **Alcohol protocol**: If consumed, neat mezcal or blanco tequila only. Two-drink maximum. Food beforehand required.
