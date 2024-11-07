import React from 'react';
import { Navigate } from 'react-router-dom';

// Funzione per controllare se l'utente è autenticato
const isAuthenticated = () => {
  const token = localStorage.getItem('token');
  return token !== null;  // Controlla se il token è presente
};

// Componente che protegge una rotta
const ProtectedRoute = ({ children }) => {
  if (!isAuthenticated()) {
    return <Navigate to="/" />;  // Se non autenticato, reindirizza alla pagina di login
  }

  return children;  // Altrimenti, mostra il contenuto della rotta protetta
};

export default ProtectedRoute;