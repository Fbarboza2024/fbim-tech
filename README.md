# 🚀 FBIM TECH — Execution Engine (Production)

Este repositório contém a **camada de execução em produção** da FBIM TECH.

Ele é responsável por:
- operar contas reais (TikTok, Instagram, Facebook, YouTube)
- publicar conteúdo automaticamente
- aplicar decisões determinísticas
- gerenciar saúde das contas
- pausar ou matar contas automaticamente
- coletar métricas
- alertar humano apenas por exceção
- operar com afiliados (links)

⚠️ Este projeto é **executor de produção**.  
Não é SaaS, não é protótipo, não é experimento.

---

## 🧠 Princípios do Projeto

- ❌ Sem microserviços
- ❌ Sem Kafka
- ❌ Sem IA interna
- ❌ Sem automação de login
- ❌ Sem senhas no código
- ✅ SQLite local
- ✅ Playwright com cookies
- ✅ Decision engine determinístico
- ✅ Humano por exceção

**Complexidade mínima ótima.**

---

## 🏗️ Arquitetura Geral



Decision Engine
↓
Runner (scheduler)
↓
Bots (TikTok / Instagram / Facebook / YouTube)
↓
Playwright (cookies + fingerprint + proxy)
↓
Plataformas


---

## 📁 Estrutura do Projeto



root/
├── Dockerfile
├── docker-compose.yml
├── package.json
├── .env.example
├── README.md
│
├── app/
│ ├── index.js
│ │
│ ├── core/
│ │ ├── browser.js # Playwright + contexto
│ │ ├── decision.engine.js # Cérebro determinístico
│ │ └── autoswap.js # Kill / swap de contas
│ │
│ ├── bots/
│ │ ├── tiktok.bot.js
│ │ ├── instagram.bot.js
│ │ ├── facebook.bot.js
│ │ └── youtube.bot.js
│ │
│ ├── workers/
│ │ └── runner.js # Loop principal
│ │
│ ├── metrics/
│ │ ├── logger.js
│ │ └── metrics.js
│ │
│ ├── notify/
│ │ └── telegram.js
│ │
│ └── storage/
│ └── db.js # SQLite (WAL)
│
├── scripts/
│ ├── generate_cookies_tiktok.js
│ ├── generate_cookies_instagram.js
│ ├── generate_cookies_facebook.js
│ ├── generate_cookies_youtube.js
│ └── renew_cookies_assisted.js
│
└── accounts/
├── production/
├── paused/
└── graveyard/


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

enviar alertas Telegram

Scheduler simples:

setInterval(loop, 60 * 1000);

🌍 Autenticação (Cookies, NÃO senha)

⚠️ O sistema NÃO faz login automático.

Padrão profissional:

login é humano

bot reutiliza sessão autenticada

cookies representam a identidade

🍪 Geração de Cookies (Manual Assistida)

Scripts disponíveis em scripts/.

TikTok
node scripts/generate_cookies_tiktok.js

Instagram
node scripts/generate_cookies_instagram.js

Facebook
node scripts/generate_cookies_facebook.js

YouTube / Google
node scripts/generate_cookies_youtube.js


Fluxo:

Navegador abre visível

Você faz login manualmente

Resolve captcha / 2FA

Pressiona ENTER

Cookies são salvos em secure/cookies/*.json

♻️ Renovação Automática Assistida

Script genérico para qualquer plataforma:

node scripts/renew_cookies_assisted.js <plataforma> <nome_da_conta>


Exemplos:

node scripts/renew_cookies_assisted.js tiktok tiktok_1
node scripts/renew_cookies_assisted.js instagram instagram_main


Usado quando:

cookie expira

conta pede reautenticação

sistema pausa automaticamente

💾 Banco de Dados (SQLite)

Arquivo: app/storage/db.js

SQLite local

WAL habilitado

sem dependência externa

Tabela principal:

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

contas mortas vão para accounts/graveyard

contas pausadas ficam fora do loop

filesystem usado como estado visível

📊 Métricas e Logs

Logs com pino

Métricas com prom-client

Contador de posts

Pronto para Prometheus

📣 Alertas Telegram

Humano é avisado apenas quando:

conta morre

conta é pausada

erro crítico acontece

cookie precisa ser renovado

Humano por exceção, não por rotina.

💰 Afiliados

O sistema usa links afiliados, não APIs.

Suportados:

Amazon

Magazine Luiza

Hotmart

ClickBank

Impact

No .env ficam apenas:

IDs

tags

nicknames

❌ Nunca senha
❌ Nunca token sensível no GitHub

🐳 Docker (Produção)

Base oficial Playwright

Chromium incluído

Restart automático

Limites de CPU e RAM

🔐 Segurança

Nenhuma senha no código

Cookies fora do GitHub

.env nunca versionado

Execução isolada em container

Adicionar ao .gitignore:

secure/cookies/
.env
data.db

🚦 Status do Projeto

✔️ Produção-ready
✔️ Determinístico
✔️ Observável
✔️ Seguro
✔️ Escalável
✔️ Sem dependência humana contínua

📌 Filosofia

Simplicidade > complexidade

Sessão válida > login automatizado

Decisão clara > IA opaca

Automação > operação manual

🏁 Conclusão

Este repositório é a camada de execução real da FBIM TECH.

Ele:

roda

publica

mede

corrige

sobrevive

Sem hype.
Sem excesso.
Código que funciona em produção.


---

✅ **README.md finalizado**  
✅ **Totalmente alinhado com o código atual**  
✅ **Pronto para copiar e colar no GitHub**  

Se quiser, o próximo (opcional) seria:
- *RUNBOOK de operação diária*
- *Checklist de primeiro deploy no VPS*
- *Manual de resposta a incidentes*

Mas **como README**, isso está **FECHADO**.


essa vps 


