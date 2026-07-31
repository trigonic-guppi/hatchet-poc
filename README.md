# Hatchet POC: Polyglot Setup

This is a proof of concept for running [Hatchet](https://hatchet.run/) as an orchestrator for a TypeScript/Python split architecture, specifically designed to be lightweight enough to run on a single Debian node via Docker Compose.

## Architecture

- **Postgres**: The single source of truth and state engine (no Redis needed).
- **Hatchet-Lite**: The unified Hatchet engine and API running in a single container.
- **TypeScript Client**: Represents the API/web layer pushing events to the queue.
- **Python Worker**: Represents the heavy/AI worker picking up events and executing multi-step durable workflows.

## Running Locally

1. **Start the engine:**
   ```bash
   docker compose up -d
   ```
   *The Hatchet dashboard will be available at http://localhost:8080*

2. **Start the Python Worker:**
   ```bash
   cd python-worker
   pip install -r requirements.txt
   export HATCHET_CLIENT_TOKEN="dummy-token-for-local-dev"
   export HATCHET_CLIENT_TLS_STRATEGY="none"
   python worker.py
   ```

3. **Push an event via TypeScript:**
   ```bash
   cd ts-client
   npm install
   export HATCHET_CLIENT_TOKEN="dummy-token-for-local-dev"
   export HATCHET_CLIENT_TLS_STRATEGY="none"
   npm start
   ```

Watch the Python worker pick up the event and execute the workflow sequentially!
