import axios from 'axios';

// Imposta l'URL base del backend
const API_URL = 'http://localhost:5001';  // Assicurati che il backend sia in esecuzione su questa porta

// Funzione per registrare un nuovo utente
export const registerUser = async (username, password) => {
    try {
        const response = await axios.post(`${API_URL}/register`, { username, password });
        return response.data;
    } catch (error) {
        console.error('Error during registration', error);
        return null;
    }
};

// Funzione per il login
export const loginUser = async (username, password) => {
    try {
        const response = await axios.post(`${API_URL}/login`, { username, password });
        return response.data.token; // Ritorna il token JWT
    } catch (error) {
        console.error('Error during login', error);
        return null;
    }
};

// Funzione per ottenere le informazioni dell'utente
export const getUserInfo = async (token) => {
    try {
        const response = await axios.get(`${API_URL}/user`, {
            headers: { Authorization: `Bearer ${token}` }
        });
        return response.data;
    } catch (error) {
        console.error('Error fetching user info', error);
        return null;
    }
};

// Funzione per effettuare una donazione
export const donate = async (token, amount) => {
    try {
        const response = await axios.post(`${API_URL}/donate`, { amount }, {
            headers: { Authorization: `Bearer ${token}` }
        });
        return response.data;
    } catch (error) {
        console.error('Error during donation', error);
        return null;
    }
};

// Funzione per comprare i prodotti se non sono esauriti
export const buyProduct = async (token, productId) => {
    try {
        const response = await axios.post(`${API_URL}/buy`, { productId }, {
            headers: { Authorization: `Bearer ${token}` }
        });
        return response.data;
    } catch (error) {
        console.error('Error during purchase', error);
        return null;
    }
};