import { db } from "../storage/db.js";
import { decide } from "../core/decision.engine.js";
import { runTikTok } from "../bots/tiktok.bot.js";
import { runYouTube } from "../bots/youtube.bot.js";
import { runInstagram } from "../bots/instagram.bot.js";
import { logger } from "../metrics/logger.js";
import { postsCounter } from "../metrics/metrics.js";
import { alert } from "../notify/telegram.js";
import { killAccount } from "../core/autoswap.js";

// loop simples e confiável
async function loop() {
  const accounts = db
    .prepare("SELECT * FROM accounts WHERE status = 'ACTIVE'")
    .all();

  for (const account of accounts) {
    try {
      const action = decide(account);

      if (action === "DEAD") {
        killAccount(account);
        db.prepare(
          "UPDATE accounts SET status='DEAD' WHERE id=?"
        ).run(account.id);
        await alert(`☠️ Conta ${account.id} morta`);
        continue;
      }

      if (action === "PAUSE") {
        db.prepare(
          "UPDATE accounts SET status='PAUSED' WHERE id=?"
        ).run(account.id);
        await alert(`⏸️ Conta ${account.id} pausada`);
        continue;
      }

      if (action === "WAIT") continue;

      // POST
      if (account.platform === "tiktok") await runTikTok(account);
      if (account.platform === "youtube") await runYouTube(account);
      if (account.platform === "instagram") await runInstagram(account);

      postsCounter.inc();

      // atualiza saúde básica
      db.prepare(
        "UPDATE accounts SET last_post=datetime('now'), health_score=health_score+0.05 WHERE id=?"
      ).run(account.id);

      logger.info({ account: account.id }, "Post executado");

    } catch (err) {
      logger.error(err, `Erro na conta ${account.id}`);

      db.prepare(
        "UPDATE accounts SET hard_failures=hard_failures+1 WHERE id=?"
      ).run(account.id);

      await alert(`❌ Erro na conta ${account.id}`);
    }
  }
}

// scheduler simples (produção-safe)
setInterval(loop, 60 * 1000);
