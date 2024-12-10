#!/bin/bash

# Funzione per controllare se il backend ha le dipendenze installate
check_backend_dependencies() {
    # Aggiungi qui la logica per verificare se le dipendenze sono installate.
    # Supponiamo che db.py dipenda da un file requirements.txt.
    if ! python3 -m pip show -r requirements.txt &> /dev/null; then
        echo "Installazione delle dipendenze del backend..."
        python3 -m pip install -r requirements.txt
    else
        echo "Le dipendenze del backend sono già installate."
    fi
}

# Funzione per controllare se il frontend ha le dipendenze installate
check_frontend_dependencies() {
    # Verifica se esiste la cartella node_modules
    if [ ! -d "node_modules" ]; then
        echo "Installazione delle dipendenze del frontend..."
        npm install
    else
        echo "Le dipendenze del frontend sono già installate."
    fi
}

# Avvia il backend
echo "Avviando il backend..."
cd fis_back/ || exit 1
check_backend_dependencies
python3 db.py &  # Esegui il comando in background

# Avvia il frontend
echo "Avviando il frontend..."
cd ../fis/ || exit 1
check_frontend_dependencies
npm start

# Attendi che il backend finisca (se necessario)
wait
