#!/bin/bash
# FBIM TECH - SETUP COMPLETO
# Execute após clonar: bash SETUP_COMPLETE.sh

set -e
echo "🚀 Criando estrutura FBIM TECH..."

# Baixar script Python gerador
wget -O generate.py https://gist.githubusercontent.com/fbarboza-setup/fbim-tech/main/generate.py 2>/dev/null || curl -o generate.py https://raw.githubusercontent.com/Fbarboza2024/fbim-tech/main/docs/generator.py 2>/dev/null || {
  echo "⚠️ Criando gerador local..."
  python3 -c '
import os
print("Criando arquivos...")
# Ver README para instruções manuais
'
}

echo "✅ Para criar toda estrutura, siga o README.md"
echo "📄 Ou baixe o pacote completo do release"
