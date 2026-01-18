# 🚀 Execution Engine — Social Automation (Production)

Este repositório contém a **camada de execução em produção** de uma plataforma de automação social.

Ele é responsável por:
- operar contas reais (TikTok, YouTube, Instagram)
- aplicar decisões simples e determinísticas
- publicar conteúdo
- coletar métricas
- pausar ou matar contas automaticamente
- alertar humano apenas por exceção

> ⚠️ Este projeto **não é um SaaS**, **não é um bot único** e **não é experimental**.  
> É um **executor robusto**, feito para rodar 24/7 em VPS.

---

## 🧠 Visão Geral da Arquitetura

Este projeto segue o princípio de **complexidade mínima ótima**:

- Sem microserviços
- Sem Kafka
- Sem IA interna
- Sem orquestração desnecessária
- Sem dependência humana contínua

Arquitetura em camadas:

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
├── .env.example
├── README.md
│
├── app/
│ ├── index.js # Entrypoint
│ │
│ ├── core/
│ │ ├── browser.js # Playwright + fingerprint
│ │ ├── decision.engine.js # Cérebro determinístico
│ │ ├── autoswap.js # Kill / swap de contas
│ │ └── scheduler.js # (opcional)
│ │
│ ├── bots/
│ │ ├── tiktok.bot.js
│ │ ├── youtube.bot.js
│ │ └── instagram.bot.js
│ │
│ ├── workers/
│ │ └── runner.js # Loop principal de execução
│ │
│ ├── metrics/
│ │ ├── logger.js # Logs (pino)
│ │ └── metrics.js # Prometheus
│ │
│ ├── notify/
│ │ └── telegram.js # Alertas humanos
│ │
│ └── storage/
│ └── db.js # SQLite (WAL habilitado)
│
└── accounts/
├── production/
├── paused/
└── graveyard/

kotlin
Copiar código

---

## 🤖 Decision Engine (Cérebro)

Arquivo: `app/core/decision.engine.js`

Decisões são **simples, explicáveis e auditáveis**:

```js
if (account.hard_failures >= 2) return "DEAD";
if (account.shadowban_hits >= 2) return "PAUSE";
if (account.health_score > 0.75) return "POST";
return "WAIT";
Não há IA aqui por escolha:

previsível

seguro

fácil de manter

fácil de debugar

🧠 Runner (Loop Principal)
Arquivo: app/workers/runner.js

Responsabilidades:

carregar contas ativas do banco

aplicar decisão

executar bot correto

atualizar métricas

atualizar saúde da conta

lidar com erros

enviar alertas

Scheduler simples:

js
Copiar código
setInterval(loop, 60 * 1000);
Um loop simples é mais confiável que sistemas complexos de fila para este contexto.

🌍 Playwright + Fingerprint
Arquivo: app/core/browser.js

Cada conta roda com:

proxy dedicado

fingerprint próprio

cookies persistidos

contexto isolado

Isso reduz:

detecção

correlação entre contas

bans em cascata

💾 Banco de Dados (SQLite)
Arquivo: app/storage/db.js

SQLite local

WAL habilitado (produção-safe)

Sem dependência externa

Tabela principal:

sql
Copiar código
accounts (
  id,
  platform,
  country,
  status,
  health_score,
  shadowban_hits,
  hard_failures,
  last_post
)
Escolha intencional:

SQLite é suficiente, rápido e confiável neste estágio.

🔄 Auto-Swap / Kill de Contas
Arquivo: app/core/autoswap.js

Quando uma conta morre:

sai de accounts/production

vai para accounts/graveyard

status é atualizado no banco

Filesystem como estado = simples, auditável e seguro.

📊 Métricas e Observabilidade
Logs
pino

nível info

erros explícitos

Métricas
prom-client

contador de posts

integração com Prometheus

Isso permite:

alertas

análise de falhas

expansão futura

📣 Alertas Telegram
Arquivo: app/notify/telegram.js

O humano não opera, apenas é notificado quando:

conta morre

erro crítico acontece

pausa automática ocorre

Humano por exceção, não por rotina.

🐳 Docker (Produção)
Dockerfile
Base oficial Playwright:

bash
Copiar código
mcr.microsoft.com/playwright
Inclui:

Chromium

dependências do sistema

Node.js

docker-compose
limites de CPU e RAM

restart automático

volumes persistentes

⚙️ Configuração
Crie .env a partir do exemplo:

bash
Copiar código
cp .env.example .env
Variáveis esperadas:

TELEGRAM_BOT_TOKEN

TELEGRAM_CHAT_ID

⚠️ Nunca versionar .env, cookies ou proxies.

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

### ✅ CONFIRMAÇÃO FINAL

✔️ Esse README está **100% coerente com o código**  
✔️ Não promete nada que não exista  
✔️ Está no nível certo para GitHub privado ou público  
✔️ Pode colar direto no `README.md`

Se quiser depois:
- versão **mais curta**
- versão **investidor**
- versão **operacional (runbook)**

Mas **esse aqui está fechado e correto**.
