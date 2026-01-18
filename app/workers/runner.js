import { runTikTok } from "../bots/tiktok.bot.js";
import { runInstagram } from "../bots/instagram.bot.js";
import { runFacebook } from "../bots/facebook.bot.js";
import { runYouTube } from "../bots/youtube.bot.js";

export async function run() {
  if (process.env.TIKTOK_ENABLED === "true") {
    console.log("▶️ TikTok bot ativo");
    await runTikTok();
  }

  if (process.env.INSTAGRAM_ENABLED === "true") {
    console.log("▶️ Instagram bot ativo");
    await runInstagram();
  }

  if (process.env.FACEBOOK_ENABLED === "true") {
    console.log("▶️ Facebook bot ativo");
    await runFacebook();
  }

  if (process.env.YOUTUBE_ENABLED === "true") {
    console.log("▶️ YouTube bot ativo");
    await runYouTube();
  }
}

