import { chromium } from "playwright";
import fs from "fs";

export async function createContext(cookiesPath) {
 const browser = await chromium.launch({
  headless: false,
  args: ["--no-sandbox", "--disable-setuid-sandbox"]
});


  const context = await browser.newContext();

  if (cookiesPath && fs.existsSync(cookiesPath)) {
    const cookies = JSON.parse(fs.readFileSync(cookiesPath));
    await context.addCookies(cookies);
  }

  return { browser, context };
}
