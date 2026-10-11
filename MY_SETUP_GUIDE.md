# Cloud Case Study – Setup Guide (Mac + Render PaaS)

Project: Restaurant Review web app deployed on a **PaaS (Render)** with a managed PostgreSQL database
Unit 2 topic: **Platform as a Service (PaaS)**
Based on Microsoft's open-source sample: github.com/Azure-Samples/msdocs-flask-postgresql-sample-app
(Azure sign-up was blocked for SRM accounts, so we deploy the same app on Render — free, no card.)

---------------------------------------------------------------------
## PART A — Run it on your Mac (local demo, ~15 min, one time)
---------------------------------------------------------------------
A1. Homebrew (skip if `brew --version` works):
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

A2. Python + PostgreSQL:
    brew install python@3.12 postgresql@16
    brew services start postgresql@16

A3. Create the database (one time):
    $(brew --prefix postgresql@16)/bin/psql postgres -c "CREATE USER app_user WITH PASSWORD 'app_password';" -c "CREATE DATABASE app OWNER app_user;"

A4. Install libraries (one time):
    cd ~/Desktop/cloud-case-study
    python3.12 -m venv .venv
    source .venv/bin/activate
    pip install Flask Flask-Migrate Flask-SQLAlchemy flask_wtf psycopg2-binary python-dotenv SQLAlchemy
    flask db upgrade

A5. Start the website:
    cd ~/Desktop/cloud-case-study
    source .venv/bin/activate
    flask run --port 8000
Open http://localhost:8000 → add a restaurant → add a review. Stop with Ctrl+C.

---------------------------------------------------------------------
## PART B — Deploy it on the cloud (Render PaaS, ~15 min, free, no card)
---------------------------------------------------------------------
B1. Put the project on YOUR GitHub
  - github.com → New repository → name: cloud-case-study → Public → do NOT add README → Create
  - In Terminal:
        cd ~/Desktop/cloud-case-study
        git remote set-url origin https://github.com/EshantSethi/cloud-case-study.git
        git push -u origin main
    (If it asks for a password, use a GitHub Personal Access Token, or run `brew install gh && gh auth login` first.)

B2. Sign up on Render
  - render.com → Get Started → **Sign up with GitHub** (no card needed)

B3. Deploy with the Blueprint (one click = whole setup)
  - Render Dashboard → **New +** → **Blueprint**
  - Connect your `cloud-case-study` repo → it reads `render.yaml`
  - Click **Apply** / **Deploy Blueprint**
  - Render creates: 1) PostgreSQL database `reviews-db`  2) web service `restaurant-reviews`
  - Wait 5–10 min → the web service shows "Live" and a URL like
    https://restaurant-reviews-xxxx.onrender.com  ← your live cloud website

B4. Screenshots to take (Implementation slides)
  1. GitHub repo showing `render.yaml` (Infrastructure as Code)
  2. Render Dashboard / Blueprint page (both resources together)
  3. Web service → Overview (status Live, region Singapore, URL)
  4. Web service → Events + Logs (build → `flask db upgrade` → gunicorn started)
  5. Web service → Environment (DATABASE_URL injected, value hidden = secrets not in code)
  6. PostgreSQL → Info (internal URL, PostgreSQL version, storage)
  7. PostgreSQL → Access Control / Networking (no public IPs allowed = private)
  8. Web service → Metrics (CPU, memory, response time)
  9. Live website with your restaurant + review (also open it on your phone)

B5. Performance test (Results slide)
    brew install hey
    hey -n 300 -c 10 https://YOUR-URL.onrender.com/
Screenshot: Requests/sec, Average, Slowest/Fastest, status codes (should all be 200).
Also note: first request after 15 min idle is slow (~1 min, "cold start") — that's a free-tier
trade-off; paid instances stay always-on. Good point for the evaluation slide.

B6. Presentation day
  - Open your Render URL **5 minutes before** class (wakes it from sleep).
  - Demo: add a restaurant + review live → show Render dashboard (Live, Logs, Metrics, Environment).
  - If asked about local development → Part A5 on localhost.

B7. After evaluation (optional clean-up)
  - Render → each service → Settings → Delete. (Free database auto-expires after 30 days anyway.)

## If something breaks
- Render build fails → open the service → Logs → send a screenshot to Claude
- Site shows "Internal Server Error" → Logs tab (usually database still starting; wait 1–2 min, Manual Deploy → Deploy latest commit)
- `git push` rejected → check the repo URL in B1 uses your username
