#!/bin/bash
set -e

echo "🚀 FBIM TECH — INSTALAÇÃO AUTOMÁTICA"

# Usuário
if ! id fbim &>/dev/null; then
  sudo useradd -m -s /bin/bash fbim
fi

sudo apt update
sudo apt install -y python3 python3-venv git

cd /home/fbim

if [ ! -d "fbim-tech" ]; then
  sudo -u fbim git clone https://github.com/Fbarboza2024/fbim-tech.git
fi

cd fbim-tech

sudo -u fbim python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Copiar services
sudo cp systemd/*.service /etc/systemd/system/
sudo systemctl daemon-reexec
sudo systemctl daemon-reload

# Subir tudo
sudo systemctl enable fbim-content
sudo systemctl enable fbim-dashboard
sudo systemctl enable fbim-redirector

sudo systemctl restart fbim-content
sudo systemctl restart fbim-dashboard
sudo systemctl restart fbim-redirector

echo "✅ FBIM TECH ONLINE"
