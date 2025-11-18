#!/bin/bash

echo "🔫 Fechando processos antigos do Chrome..."
pkill chrome
pkill chromium

echo "🌐 Abrindo Chrome em modo Debug (porta 9222)..."
nohup /opt/google/chrome/google-chrome \
    --remote-debugging-port=9222 \
    --user-data-dir="/home/tayara/.config/google-chrome" \
    >/dev/null 2>&1 &

echo "⏳ Aguardando Chrome iniciar..."
sleep 3

echo "🐍 Ativando ambiente virtual..."
source venv/bin/activate

echo "🚀 Iniciando script vagas.py..."
python3 vagas.py
