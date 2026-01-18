import "dotenv/config";
import { run } from "./workers/runner.js";

console.log("🚀 FBIM TECH — Social Automation Online");

run().catch(err => {
  console.error("❌ Fatal error in FBIM:", err);
  process.exit(1);
});
