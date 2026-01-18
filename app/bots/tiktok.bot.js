import { createContext } from "../core/browser.js";

export async function runTikTok() {
  const cookies = process.env.TIKTOK_1_COOKIES;

  const { browser, context } = await createContext(cookies);
  const page = await context.newPage();

  console.log("📲 TikTok — abrindo feed");
  await page.goto("https://www.tiktok.com", { waitUntil: "domcontentloaded" });

  // Aqui entra upload / post / scrape depois

  await browser.close();
}
