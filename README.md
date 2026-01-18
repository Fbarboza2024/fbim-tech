# FBIM TECH

> **Empresa Algorítmica Autônoma, Antifrágil e Auto‑Governada**

FBIM TECH é uma plataforma de automação avançada que opera como uma **empresa viva**: cria bots, testa estratégias, escala o que dá lucro, mata o que não funciona e se protege automaticamente contra falhas, prejuízos e bugs.

Este repositório contém **toda a arquitetura final**, pronta para produção, com:

* governança algorítmica
* auditoria automática
* kill‑switch global
* rollback automático
* chaos engineering

---

## 🧠 VISÃO GERAL

A FBIM TECH não é um bot.
É um **organismo computacional** composto por múltiplas camadas:

```
EXECUÇÃO  →  GOVERNANÇA  →  AUDITORIA  →  AUTOPROTEÇÃO
```

Tudo roda **24/7**, sem intervenção humana, exceto quando estritamente necessário.

---

## 🏗️ ARQUITETURA FINAL

```
fbim-tech/
├── docker-compose.yml
├── README.md
├── .env.example
├── .gitignore
│
├── data/                     # Estado global (persistente)
│   └── global_state.json
│
├── logs/
│
├── fbim/                     # CORE DE NEGÓCIO
│   ├── audit/
│   ├── feedback/
│   ├── scheduler/
│   ├── sandbox/
│   ├── lifecycle/
│   ├── copy/
│   ├── funnels/
│   ├── monetization/
│   ├── redirector/
│   ├── paid_traffic/
│   ├── ltv/
│   ├── spin/
│   ├── i18n/
│   └── dashboard/
│
├── bots/                     # BOTS EXECUTORES
│   ├── bot_futures.py
│   ├── content_engine.py
│   └── telegram_notifier.py
│
├── governance/               # CÉREBRO DA EMPRESA
│   ├── core/                 # Estado, eventos, registry
│   ├── hr_bot/               # Vida e morte de bots
│   ├── finance_bot/          # CFO algorítmico
│   ├── ai_strategist/        # Estratégia agressiva
│   ├── auto_scale/           # Escala por lucro
│   ├── lab_bot/              # Experimentos econômicos
│   ├── audit_bot/            # Auditoria mensal
│   ├── health_score/         # Score 0–100 da empresa
│   ├── kill_switch/          # Proteção global
│   ├── rollback/             # Rollback automático
│   └── chaos_bot/            # Chaos Engineering
│
└── .github/workflows/
    └── deploy.yml
```

---

## 🤖 CAMADAS E RESPONSABILIDADES

### 🔹 Execução (`bots/`)

* Trading
* Conteúdo
* Tráfego
* Monetização

Nunca decidem nada sozinhos.

---

### 🔹 Governança (`governance/`)

| Serviço       | Função                       |
| ------------- | ---------------------------- |
| HR Bot        | Ativa, pausa ou mata bots    |
| Finance Bot   | Consolida PnL e risco        |
| AI Strategist | Decide onde escalar          |
| Auto Scale    | Solicita aumento de recursos |
| Lab Bot       | Cria experimentos            |
| Audit Bot     | Auditoria mensal             |
| Health Score  | Saúde da empresa (0–100)     |
| Kill‑Switch   | Pausa tudo em crise          |
| Rollback      | Volta versão ruim            |
| Chaos Bot     | Testa falhas reais           |

---

## 📊 SCORE DE SAÚDE (0–100)

O **Health Score** é calculado automaticamente com base em:

* lucro
* drawdown
* bots ativos
* governança viva
* crescimento
* dependência humana

| Score  | Estado      |
| ------ | ----------- |
| 85–100 | 🟢 Saudável |
| 70–84  | 🟡 Estável  |
| 50–69  | 🟠 Risco    |
| < 50   | 🔴 Crítico  |

---

## 🚨 KILL‑SWITCH GLOBAL

Dispara automaticamente quando:

* Health Score < limite
* drawdown extremo
* falha sistêmica

Ação:

* pausa bots executores
* mantém governança viva
* aguarda recuperação
* religa tudo sozinho

---

## 🔄 ROLLBACK AUTOMÁTICO

Todo deploy segue o fluxo:

```
Deploy → candidate
Avaliação
→ aprovado → stable
→ ruim → rollback automático
```

Nenhuma versão ruim escala.

---

## 🌪️ CHAOS ENGINEERING

Uma vez por período:

* falha controlada é injetada
* container é parado ou reiniciado
* sistema deve se recuperar sozinho

Objetivo:

> **Eliminar surpresas em produção**

---

## 🚀 INSTALAÇÃO (SSH / VPS)

### 1️⃣ Requisitos

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install docker docker-compose git -y
```

### 2️⃣ Clonar repositório

```bash
git clone https://github.com/SEU_USUARIO/fbim-tech.git
cd fbim-tech
```

### 3️⃣ Configurar ambiente

```bash
cp .env.example .env
nano .env
```

### 4️⃣ Subir tudo

```bash
docker compose up -d --build
```

---

## 🔐 SEGURANÇA

* `.env` nunca versionado
* repositório privado
* acesso SSH por chave
* kill‑switch ativo
* rollback automático

---

## 🧠 FILOSOFIA DO PROJETO

* Bots são descartáveis
* Lucro manda
* Falha pequena é aprendizado
* Falha grande é inaceitável
* Humano só por exceção

---

## 🏁 STATUS DO PROJETO

✔️ Produção‑ready
✔️ Antifrágil
✔️ Auto‑governado
✔️ Escalável
✔️ Sem ponto único de falha

---

## 📌 CONCLUSÃO

FBIM TECH não é um script.

É uma **empresa algorítmica completa**, projetada para:

* crescer sozinha
* se corrigir sozinha
* sobreviver a falhas reais

> **99% dos projetos nunca chegam aqui.**
