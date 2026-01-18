import { chromium } from "playwright";
import fs from "fs";
import path from "path";

const ACCOUNT_NAME = "youtube_main";
const OUTPUT_DIR = "./secure/cookies";
const LOGIN_URL = "https://accounts.google.com/";

fs.mkdirSync(OUTPUT_DIR, { recursive: true });

(async () => {
  const browser = await chromium.launch({ headless: false, slowMo: 50 });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 },
    locale: "en-US"
  });

  const page = await context.newPage();
  await page.goto(LOGIN_URL, { waitUntil: "networkidle" });

  console.log("🔐 Faça login Google (YouTube)");
  console.log("👉 Resolva tudo manualmente");
  console.log("👉 Pressione ENTER quando concluir");

  process.stdin.resume();
  await new Promise(r => process.stdin.once("data", r));

  const output = path.join(OUTPUT_DIR, `${ACCOUNT_NAME}.json`);
  await context.storageState({ path: output });

  console.log(`✅ Cookies salvos em ${output}`);
  await browser.close();
})();
