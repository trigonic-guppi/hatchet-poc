# 🚀 Ube V1 Architecture: The Case for Hatchet

Hey Orkun, based on your notes about the TS/Python split, the need for durable execution (rate limits/retries), and the goal of starting on a **single Debian box**, we put together a working proof-of-concept using Hatchet.

Here is the breakdown of why this fits perfectly for V1, and how you can test it yourself in 2 minutes.

---

## 1. The "Single Debian Box" Constraint
Temporal is the undisputed heavyweight champion, but self-hosting it requires a massive DevOps tax (History service, Matching service, Frontend, internal workers, plus DB and usually Elasticsearch). 

**Hatchet is Temporal without the DevOps nightmare.** 
It gives us the exact same durable execution model, but it runs entirely on a **single Postgres instance**. We can spin the entire orchestrator up on that Debian box using a simple Docker Compose file. No Redis, no Cassandra, no cluster management.

## 2. Polyglot Harmony (TypeScript + Python)
We built the POC to mirror exactly what we discussed:
*   **TypeScript (API/Ingestion):** A lightweight client that catches webhooks and pushes events to the queue.
*   **Python (AI/Workers):** A heavy worker that picks up the events, manages the LLM context, and executes the workflows.

## 3. Resilience: Meta API & LLM Rate Limits
You mentioned needing global rate limits and retries for external APIs. Hatchet has this built-in natively. 
In the POC, we explicitly simulate a flaky API (50% failure rate). You can watch Hatchet catch the failure, back off, and retry the step automatically without writing any custom retry logic.

## 4. What about Braintrust?
We don't actually need Temporal's native integration to use Braintrust for LLM evals. Braintrust is ultimately just an SDK. We can drop the `braintrust` Python package directly into our Hatchet workers to trace the LLM calls, log scores, and build our eval sets with zero friction.

---

## 🎮 Run the 2-Minute Demo

I’ve set this up so you can run it right now and watch it work. 

**1. Start the Hatchet Engine (Docker)**
```bash
git clone https://github.com/trigonic-guppi/hatchet-poc.git
cd hatchet-poc
docker compose up -d
```
*Open `http://localhost:8080` to see the Hatchet Dashboard.*

**2. Start the Python AI Worker**
*(In a new terminal)*
```bash
cd python-worker
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
export HATCHET_CLIENT_TOKEN="dummy-token-for-local-dev"
export HATCHET_CLIENT_TLS_STRATEGY="none"
python worker.py
```
*Notice it instantly registers the workflows and starts a Cron job.*

**3. Spike the Traffic (TypeScript)**
*(In a third terminal)*
```bash
cd ../ts-client
npm install
export HATCHET_CLIENT_TOKEN="dummy-token-for-local-dev"
export HATCHET_CLIENT_TLS_STRATEGY="none"
npm start
```

### What to watch for:
1. The TS client fires **5 concurrent events** simulating a traffic spike.
2. The Python worker picks them up. 
3. Watch the terminal (and the web UI) as the simulated "flaky API" causes random tasks to fail. **Watch Hatchet automatically retry them until they turn green.**

**Verdict:** Let's start with Hatchet for V1. If we outgrow it, we can migrate to Temporal Cloud when the user base and revenue justify it.
