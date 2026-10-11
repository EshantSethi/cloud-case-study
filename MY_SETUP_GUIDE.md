# Cloud Case Study – Setup Guide (Mac + Azure)

Project: Restaurant Review web app on **Azure App Service (PaaS)** + PostgreSQL
Unit 2 topic: **Platform as a Service (PaaS)**
Based on Microsoft's open-source sample: github.com/Azure-Samples/msdocs-flask-postgresql-sample-app

Open Terminal and run the blocks in order. Copy each block fully.

---------------------------------------------------------------------
## PART A — Run it on your Mac (local demo, ~15 min, one time)
---------------------------------------------------------------------

### A1. Install Homebrew (skip if `brew --version` already works)
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

### A2. Install Python + PostgreSQL and start the database
    brew install python@3.12 postgresql@16
    brew services start postgresql@16

### A3. Create the database the app expects (one time)
    $(brew --prefix postgresql@16)/bin/psql postgres -c "CREATE USER app_user WITH PASSWORD 'app_password';" -c "CREATE DATABASE app OWNER app_user;"

### A4. Install the app's libraries (one time)
    cd ~/Desktop/cloud-case-study
    python3.12 -m venv .venv
    source .venv/bin/activate
    pip install Flask Flask-Migrate Flask-SQLAlchemy flask_wtf psycopg2-binary python-dotenv SQLAlchemy
    flask db upgrade

(We use psycopg2-binary on Mac so nothing needs compiling. Don't edit requirements.txt — Azure uses it.)

### A5. Start the website  ← do THIS on presentation day
    cd ~/Desktop/cloud-case-study
    source .venv/bin/activate
    flask run --port 8000

Open http://localhost:8000 → add a restaurant → add a review. Stop with Ctrl+C.

---------------------------------------------------------------------
## PART B — Deploy it on Azure (real cloud, ~20 min)
---------------------------------------------------------------------

### B1. Activate Azure for Students (no card)
Go to https://azure.microsoft.com/free/students → sign in with your SRM email → verify.

### B2. Install the Azure Developer CLI
    brew tap azure/azd && brew install azd

### B3. Log in
    azd auth login

### B4. Deploy everything with ONE command
    cd ~/Desktop/cloud-case-study
    azd up

It will ask:
- Environment name → type: fest-reviews   (any short name)
- Subscription → pick "Azure for Students"
- Location → pick **Central India** (if it fails with a region/policy error, run `azd up` again and pick South India or East Asia)

Wait 15–25 min. At the end it prints a URL like https://xxxx.azurewebsites.net → that's your live cloud website. Open it on your phone too!

### B5. Screenshots to take (for the Implementation slides)
In https://portal.azure.com → Resource groups → rg-fest-reviews:
1. The resource group list (shows all services together)
2. App Service → Overview (PaaS, URL, status "Running")
3. App Service plan → Scale up / Scale out pages (scalability)
4. Azure Database for PostgreSQL → Overview + Networking (private access)
5. Virtual network → Subnets / Private endpoints (networking)
6. Key Vault → Overview (security)
7. App Service → Configuration / Environment variables (connection settings, no passwords in code)
8. Application Insights → Performance / Live metrics (response time)
9. The live website with your added restaurant + review
10. Cost Management → Cost analysis (after 1 day)

### B6. Quick performance test (for the Results slide)
    brew install hey
    hey -n 500 -c 20 https://YOUR-URL.azurewebsites.net/

Screenshot the summary (requests/sec, average latency). Then in Portal → App Service plan → Scale out → set 2 instances → run the same command again and compare.

### B7. IMPORTANT — delete after your presentation (stops spending credit)
    cd ~/Desktop/cloud-case-study
    azd down --purge

---------------------------------------------------------------------
## Presentation-day demo (2 minutes)
---------------------------------------------------------------------
1. Open the Azure URL → show the live site → add a restaurant + a review live.
2. Show Azure Portal → resource group → App Service → App Insights live metrics.
3. If the teacher asks about local dev → show `flask run` on localhost (Part A5).

## If something breaks
- "port 8000 in use" → use `flask run --port 8001`
- "role app_user does not exist" → redo step A3
- `azd up` region/quota error → `azd up` again with another location
- Site shows error on Azure → Portal → App Service → Log stream
