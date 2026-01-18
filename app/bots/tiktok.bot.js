import { createContext } from "../core/browser.js";

export async function runTikTok() {
  const cookiesPath = process.env.TIKTOK_1_COOKIES;

  if (!cookiesPath) {
    throw new Error("TIKTOK_1_COOKIES não definido no .env");
  }

  const { browser, context } = await createContext(cookiesPath);
  const page = await context.newPage();

  console.log("📲 TikTok — abrindo feed");
  await page.goto("https://www.tiktok.com", { waitUntil: "domcontentloaded" });

  // Aqui entra upload / post / scrape depois

  await browser.close();
}
