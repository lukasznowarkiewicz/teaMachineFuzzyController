#!/bin/bash

# Navigacja do lokalizacji, gdzie jest repozytorium
cd ~/repo/iss_proj

# Pobieranie aktualizacji z repozytorium GitHub
git pull

# Otwieranie przeglądarki Chromium w trybie kiosku
# Opcje --noerrdialogs, --disable-infobars i --check-for-update-interval=31536000
# służą do wyłączenia dialogów błędów, pasków informacyjnych i aktualizacji
chromium-browser --kiosk 'file://~/repo/iss_proj/web_app/index.html' --noerrdialogs --disable-infobars --check-for-update-interval=31536000 &

# Uruchomienie aplikacji main.py
python3 python_desktop_app/main.py &

