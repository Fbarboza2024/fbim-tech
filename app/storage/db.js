import Database from "better-sqlite3";

export const db = new Database("data.db");

// PRODUÇÃO: evita lock
db.pragma("journal_mode = WAL");

// garante tabela
db.prepare(`
  CREATE TABLE IF NOT EXISTS accounts (
    id TEXT PRIMARY KEY,
    platform TEXT,
    country TEXT,
    status TEXT,
    health_score REAL DEFAULT 0.5,
    shadowban_hits INTEGER DEFAULT 0,
    hard_failures INTEGER DEFAULT 0,
    last_post DATETIME
  )
`).run();
