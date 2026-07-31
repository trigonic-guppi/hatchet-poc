import asyncio
from hatchet_sdk import Hatchet

# The SDK will automatically pick up HATCHET_CLIENT_TOKEN and HATCHET_CLIENT_TLS_STRATEGY=none
# from the environment when running locally against the dummy docker-compose.
hatchet = Hatchet(debug=True)

@hatchet.workflow(on_events=["user:created"])
class UserCreatedWorkflow:
    @hatchet.step()
    def process_user_data(self, context):
        user_id = context.workflow_input()["userId"]
        print(f"Processing data for user {user_id}")
        return {"status": "data processed"}

    @hatchet.step(parents=["process_user_data"])
    def generate_llm_response(self, context):
        print("Mocking LLM generation with global rate limits...")
        # Rate limiting and retries go here
        return {"llm_output": "Welcome to the platform!"}

def main():
    worker = hatchet.worker("python-ai-worker")
    worker.register_workflow(UserCreatedWorkflow())
    print("Starting Python worker...")
    worker.start()

if __name__ == "__main__":
    main()
