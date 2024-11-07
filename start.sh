#!/bin/bash

# Avvia il backend
echo "Avviando il backend..."
cd fis_back/ &&  python3 db.py &  # Il simbolo & esegue il comando in background

# Avvia il frontend
echo "Avviando il frontend..."
cd fis/ &&  npm start

# Attendi che il backend finisca (se necessario)
wait
