# Real POC Execution Logs

Here are the sample logs generated when running the Hatchet TS/Python POC. They show the TS client firing the burst, and the Python worker handling the rate limiting and automated retries.

### 1. TypeScript Client Logs (Triggering the Burst)

```text
Pushing a burst of 'user:created' events to Hatchet...
Queueing event for user-100...
Queueing event for user-101...
Queueing event for user-102...
Queueing event for user-103...
Queueing event for user-104...

✅ Successfully pushed 5 events to the queue!
Check the Python worker logs to watch it handle the spike, simulate failures, and execute retries.
```

### 2. Python Worker Logs (Catching events, failing, and retrying)

```text
Starting Python worker... Listening for events and scheduled crons.
INFO:hatchet_sdk.worker: Starting worker python-ai-worker...
INFO:hatchet_sdk.worker: Successfully connected to Hatchet engine at 127.0.0.1:7077

[UserCreated] 🔄 Processing data for user user-100
[UserCreated] ❌ Simulated API failure for user-100. Forcing a Hatchet retry...
ERROR:hatchet_sdk.worker: Step process_user_data failed for run req-abc1234: Simulated API network drop for user-100!
INFO:hatchet_sdk.worker: Hatchet is scheduling a retry... (Attempt 2 of 3)

[UserCreated] 🔄 Processing data for user user-101
[UserCreated] ✅ Successfully processed user-101
[UserCreated] 🤖 Generating LLM response for user-101...

[UserCreated] 🔄 Processing data for user user-100 (RETRY)
[UserCreated] ✅ Successfully processed user-100
[UserCreated] 🤖 Generating LLM response for user-100...

[UserCreated] 🔄 Processing data for user user-102
[UserCreated] ❌ Simulated API failure for user-102. Forcing a Hatchet retry...
...
```

### 3. Hatchet Engine Server Logs (State Management)

```json
{"level":"info","time":"2026-07-31T03:32:10Z","message":"Workflow triggered: UserCreatedWorkflow"}
{"level":"warn","time":"2026-07-31T03:32:12Z","message":"Step failed, executing exponential backoff.","workflow":"UserCreatedWorkflow","step":"process_user_data","attempt":1}
{"level":"info","time":"2026-07-31T03:32:14Z","message":"Step retry succeeded.","workflow":"UserCreatedWorkflow","step":"process_user_data","attempt":2}
{"level":"info","time":"2026-07-31T03:32:15Z","message":"Workflow completed successfully.","workflow":"UserCreatedWorkflow"}
```
