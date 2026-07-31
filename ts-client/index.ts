import { Hatchet } from '@hatchet-dev/typescript-sdk';
import * as dotenv from 'dotenv';

dotenv.config();

const hatchet = Hatchet.init();

async function main() {
  console.log("Pushing a burst of 'user:created' events to Hatchet...");
  
  // Fire off 5 events concurrently to simulate a traffic spike
  // Hatchet will queue these and process them based on the worker's capacity
  const promises = Array.from({ length: 5 }).map((_, i) => {
    const userId = `user-${100 + i}`;
    console.log(`Queueing event for ${userId}...`);
    
    return hatchet.event.push('user:created', {
      userId: userId,
      email: `test${i}@example.com`
    });
  });
  
  await Promise.all(promises);
  console.log('\n✅ Successfully pushed 5 events to the queue!');
  console.log('Check the Python worker logs to watch it handle the spike, simulate failures, and execute retries.');
}

main().catch(console.error);
