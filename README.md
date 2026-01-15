# FBIM TECH

**Futures Bot with Intelligent Monitoring**

Sistema automatizado de trading de futuros com controle de risco, governança e notificações.

## 🚀 Instalação Rápida

```bash
# No VPS
git clone git@github.com:Fbarboza2024/fbim-tech.git
cd fbim-tech
bash scripts/install.sh
```

## 📁 Estrutura

```
fbim-tech/
├── fbim/
│   ├── config.py          # Configurações
│   ├── db.py              # Banco de dados
│   ├── risk/engine.py     # Engine de risco
│   ├── trading/futures.py # Execução de trades
│   ├── infra/telegram.py  # Notificações
│   └── governance/guard.py # Validações
├── services/
│   ├── bot_futures.py     # Bot principal (Flask webhook)
│   ├── risk_observer.py   # Monitor de risco
│   └── telegram_notifier.py # Notificador
├── scripts/
│   ├── install.sh         # Instalador automático
│   ├── setup_env.sh       # Cria .env
│   └── setup_systemd.sh   # Configura systemd
└── requirements.txt
```

## ⚙️ Configuração

Edite `.env`:

```bash
MODE=OBSERVATION  # ou REAL
LEVERAGE=10
WEBHOOK_TOKEN=seu_token_seguro

BINANCE_API_KEY=
BINANCE_API_SECRET=

BYBIT_API_KEY=
BYBIT_API_SECRET=

TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
```

## 🎯 Como Funciona

1. **TradingView** envia sinal via webhook → `http://seu-vps:5000/webhook`
2. **GovernanceGuard** valida token e modo de operação
3. **RiskEngine** verifica limites de drawdown
4. **FuturesTrader** executa na Binance ou Bybit
5. **Telegram** notifica cada ação

## 🛡️ Segurança

- Modo OBSERVATION por padrão (não opera real)
- Limites de risco configuráveis
- Validação de token em cada webhook
- Logs completos no SQLite

## 📊 Monitoramento

```bash
# Status dos serviços
systemctl status fbim-bot fbim-risk fbim-telegram

# Logs em tempo real
journalctl -u fbim-bot -f
```

## 🔧 Manutenção

```bash
# Reiniciar serviços
sudo systemctl restart fbim-bot

# Ver trades
sqlite3 trades.db "SELECT * FROM trades ORDER BY timestamp DESC LIMIT 10;"
```

---

**Desenvolvido para traders profissionais** • Privado • Automatizado
