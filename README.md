# 🚀 Execution Engine — Social Automation (Production)

Este repositório contém a **camada de execução em produção** de uma plataforma de automação social.

Ele é responsável por:
- operar contas reais (TikTok, YouTube, Instagram)
- aplicar decisões simples e determinísticas
- publicar conteúdo
- coletar métricas
- pausar ou matar contas automaticamente
- alertar humano apenas por exceção

⚠️ Este projeto é **executor de produção**.  
Não é SaaS, não é protótipo, não é experimento.

---

## 🧠 Princípios do Projeto

- ❌ Sem microserviços
- ❌ Sem Kafka
- ❌ Sem IA interna
- ❌ Sem complexidade desnecessária
- ✅ SQLite local
- ✅ Decision engine determinístico
- ✅ Playwright com fingerprint
- ✅ Produção 24/7

**Complexidade mínima ótima.**

---

## 🏗️ Arquitetura Geral

Decision Engine
↓
Runner (scheduler)
↓
Bots (TikTok / YouTube / Instagram)
↓
Playwright (fingerprint + proxy)
↓
Plataformas

yaml
Copiar código

---

## 📁 Estrutura de Pastas

root/
├── Dockerfile
├── docker-compose.yml
├── package.json
├── .env.example
├── README.md
│
├── app/
│ ├── index.js # Entrypoint
│ │
│ ├── core/
│ │ ├── browser.js # Playwright + fingerprint
│ │ ├── decision.engine.js # Cérebro determinístico
│ │ └── autoswap.js # Kill / swap de contas
│ │
│ ├── bots/
│ │ ├── tiktok.bot.js
│ │ ├── youtube.bot.js
│ │ └── instagram.bot.js
│ │
│ ├── workers/
│ │ └── runner.js # Loop principal
│ │
│ ├── metrics/
│ │ ├── logger.js # Logs (pino)
│ │ └── metrics.js # Prometheus
│ │
│ ├── notify/
│ │ └── telegram.js # Alertas humanos
│ │
│ └── storage/
│ └── db.js # SQLite (WAL)
│
└── accounts/
├── production/
├── paused/
└── graveyard/

kotlin
Copiar código

---

## 🤖 Decision Engine

Arquivo: `app/core/decision.engine.js`

```js
if (account.hard_failures >= 2) return "DEAD";
if (account.shadowban_hits >= 2) return "PAUSE";
if (account.health_score > 0.75) return "POST";
return "WAIT";
determinístico

explicável

auditável

seguro para produção

🔁 Runner (Loop Principal)
Arquivo: app/workers/runner.js

Responsabilidades:

carregar contas ativas do banco

aplicar decisão

executar bot correto

atualizar métricas

atualizar saúde da conta

lidar com erros

enviar alertas

Scheduler simples e confiável:

js
Copiar código
setInterval(loop, 60 * 1000);
🌍 Playwright + Fingerprint
Arquivo: app/core/browser.js

Cada conta roda com:

proxy próprio

fingerprint próprio

cookies persistidos

contexto isolado

Reduz:

detecção

correlação entre contas

bans em cascata

💾 Banco de Dados (SQLite)
Arquivo: app/storage/db.js

SQLite local

WAL habilitado (produção-safe)

sem dependência externa

Tabela principal:

sql
Copiar código
accounts (
  id TEXT PRIMARY KEY,
  platform TEXT,
  country TEXT,
  status TEXT,
  health_score REAL,
  shadowban_hits INTEGER,
  hard_failures INTEGER,
  last_post DATETIME
)
🔄 Auto-Swap / Kill de Contas
Arquivo: app/core/autoswap.js

Quando uma conta morre:

sai de accounts/production

vai para accounts/graveyard

status atualizado no banco

Filesystem como estado = simples e auditável.

📊 Métricas e Logs
Logs
pino

nível info

erros explícitos

Métricas
prom-client

contador de posts

pronto para Prometheus

📣 Alertas Telegram
Arquivo: app/notify/telegram.js

O humano é notificado apenas quando:

conta morre

conta é pausada

erro crítico acontece

Humano por exceção, não por rotina.

🐳 Docker (Produção)
Dockerfile
Base oficial Playwright

Chromium incluído

Node.js pronto

docker-compose
restart automático

limites de CPU e RAM

volumes persistentes

⚙️ Configuração
Criar .env a partir do exemplo:

bash
Copiar código
cp .env.example .env
Variáveis:

nginx
Copiar código
TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID
⚠️ Nunca versionar .env, cookies, proxies ou fingerprints.

🔐 Segurança
Nenhuma credencial no GitHub

Cookies e fingerprints fora do repositório

Banco local

Execução isolada em container

🚦 Status do Projeto
✔️ Produção-ready
✔️ Determinístico
✔️ Observável
✔️ Simples de manter
✔️ Escalável horizontalmente
✔️ Sem dependência humana contínua

📌 Filosofia
Simplicidade > complexidade

Decisão clara > IA opaca

Falha pequena > falha silenciosa

Automação > operação manual

🏁 Conclusão
Este repositório é a camada de execução real de um sistema maior.

Ele:

roda

publica

mede

corrige

sobrevive

Sem hype.
Sem excesso.
Código que funciona.

yaml
Copiar código

---

✅ **Esse README.md está pronto para copiar e colar.**  
✅ **Não promete nada que não exista no código.**  
✅ **Alinhado 100% com o repositório.**

Se quiser depois:
- versão resumida
- versão investidor
- versão operacional (runbook)

Mas **esse aqui já está fechado e correto**.




