import { Hatchet } from '@hatchet-dev/typescript-sdk';
import * as dotenv from 'dotenv';

dotenv.config();

// The SDK automatically picks up environment variables.
const hatchet = Hatchet.init();

async function main() {
  console.log("Pushing 'user:created' event to Hatchet...");
  const event = await hatchet.event.push('user:created', {
    userId: 'user-123',
    email: 'test@example.com'
  });
  
  console.log('Successfully pushed event!', event);
}

main().catch(console.error);
