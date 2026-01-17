#!/bin/bash
set -e

sudo apt update
sudo apt install -y python3 python3-venv git

git clone https://github.com/SEU_USUARIO/fbim-tech.git || true
cd fbim-tech

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

sudo cp systemd/*.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable fbim-content
sudo systemctl restart fbim-content
