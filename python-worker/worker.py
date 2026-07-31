import random
from hatchet_sdk import Hatchet, Context

# The SDK will automatically pick up HATCHET_CLIENT_TOKEN and HATCHET_CLIENT_TLS_STRATEGY=none
hatchet = Hatchet(debug=True)

# 1. Event-Triggered Workflow with Retries (Simulates Meta API/LLM calls)
@hatchet.workflow(on_events=["user:created"])
class UserCreatedWorkflow:
    
    # We set retries=3 here. Hatchet will automatically back off and retry this step if it fails.
    @hatchet.step(retries=3)
    def process_user_data(self, context: Context):
        user_id = context.workflow_input()["userId"]
        print(f"\n[UserCreated] 🔄 Processing data for user {user_id}")
        
        # Simulate a flaky API (like Meta) that randomly drops requests
        if random.random() < 0.5:
            print(f"[UserCreated] ❌ Simulated API failure for {user_id}. Forcing a Hatchet retry...")
            raise Exception(f"Simulated API network drop for {user_id}!")
            
        print(f"[UserCreated] ✅ Successfully processed {user_id}")
        return {"status": "data processed", "user_id": user_id}

    @hatchet.step(parents=["process_user_data"])
    def generate_llm_response(self, context: Context):
        # We fetch the output from the previous step seamlessly
        user_id = context.step_output("process_user_data")["user_id"]
        print(f"[UserCreated] 🤖 Generating LLM response for {user_id}...")
        
        # In a real app, you can apply Hatchet global rate limiting to this specific step
        # to ensure you never exceed Anthropic/OpenAI's TPM limits.
        return {"llm_output": f"Welcome to the platform, {user_id}!"}


# 2. Cron-Triggered Workflow (Simulates background syncing)
@hatchet.workflow(on_crons=["* * * * *"]) # Runs every 60 seconds automatically
class BackgroundSyncWorkflow:
    @hatchet.step()
    def sync_records(self, context: Context):
        print("\n[Cron] ⏰ Running background sync workflow...")
        return {"synced_records": 42, "status": "success"}


def main():
    worker = hatchet.worker("python-ai-worker")
    worker.register_workflow(UserCreatedWorkflow())
    worker.register_workflow(BackgroundSyncWorkflow())
    print("Starting Python worker... Listening for events and scheduled crons.")
    worker.start()

if __name__ == "__main__":
    main()
