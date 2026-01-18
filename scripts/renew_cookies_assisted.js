import { chromium } from "playwright";
import fs from "fs";
import path from "path";

const PLATFORM = process.argv[2]; // tiktok | instagram | facebook | youtube
const ACCOUNT = process.argv[3];  // nome do arquivo
const LOGIN_URLS = {
  tiktok: "https://www.tiktok.com/login",
  instagram: "https://www.instagram.com/accounts/login/",
  facebook: "https://www.facebook.com/login",
  youtube: "https://accounts.google.com/"
};

if (!PLATFORM || !ACCOUNT) {
  console.log("Uso: node renew_cookies_assisted.js <platform> <account_name>");
  process.exit(1);
}

const OUTPUT_DIR = "./secure/cookies";
fs.mkdirSync(OUTPUT_DIR, { recursive: true });

(async () => {
  console.log(`♻️ Renovação assistida: ${PLATFORM} / ${ACCOUNT}`);

  const browser = await chromium.launch({ headless: false, slowMo: 50 });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 }
  });

  const page = await context.newPage();
  await page.goto(LOGIN_URLS[PLATFORM], { waitUntil: "networkidle" });

  console.log("🔐 Faça login manual");
  console.log("👉 Pressione ENTER ao finalizar");

  process.stdin.resume();
  await new Promise(r => process.stdin.once("data", r));

  const output = path.join(OUTPUT_DIR, `${ACCOUNT}.json`);
  await context.storageState({ path: output });

  console.log(`✅ Cookies renovados: ${output}`);
  await browser.close();
})();
