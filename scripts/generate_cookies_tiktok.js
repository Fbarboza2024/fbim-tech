import { chromium } from "playwright";
import fs from "fs";
import path from "path";

// ===== CONFIGURAÇÕES =====
const ACCOUNT_NAME = "tiktok_1"; // nome do arquivo
const OUTPUT_DIR = "./secure/cookies";
const LOGIN_URL = "https://www.tiktok.com/login";

// cria pasta se não existir
fs.mkdirSync(OUTPUT_DIR, { recursive: true });

(async () => {
  console.log("🚀 Abrindo navegador para login manual...");

  const browser = await chromium.launch({
    headless: false, // SEMPRE false
    slowMo: 50       // comportamento humano
  });

  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 },
    locale: "en-US"
  });

  const page = await context.newPage();
  await page.goto(LOGIN_URL, { waitUntil: "networkidle" });

  console.log("🔐 FAÇA LOGIN MANUALMENTE NO TIKTOK");
  console.log("👉 Resolva captcha / 2FA se aparecer");
  console.log("👉 Quando estiver LOGADO, volte aqui");

  // espera você confirmar no terminal
  process.stdin.resume();
  await new Promise(resolve => {
    process.stdin.once("data", resolve);
  });

  const storagePath = path.join(
    OUTPUT_DIR,
    `${ACCOUNT_NAME}.json`
  );

  await context.storageState({ path: storagePath });

  console.log(`✅ Cookies salvos em: ${storagePath}`);
  console.log("🔒 Agora o bot pode usar essa conta sem senha.");

  await browser.close();
  process.exit(0);
})();
