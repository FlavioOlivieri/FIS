import React, { useState } from "react";
import { Dialog } from 'primereact/dialog';
import { FloatLabel } from 'primereact/floatlabel';
import { InputText } from "primereact/inputtext";
import { Button } from 'primereact/button';
import axios from 'axios';
import '../css/Donate.css';

const API_URL = 'http://192.168.1.9:5001';  // URL del backend

export default function Donate({ visible, onHide, position, updateSaldo }) {
    const [value, setValue] = useState('');
    const [error, setError] = useState(null);
    const [successMessage, setSuccessMessage] = useState('');

    const handleDonate = async () => {
        if (!value || isNaN(value)) {
            setError('Inserisci un valore numerico valido');
            return;
        }
    
        try {
            const token = localStorage.getItem('token');  // Recupera il token dal localStorage
            const response = await axios.post(`${API_URL}/donate`, {
                amount: parseFloat(value),  // Converti la donazione in un numero e usa 'saldo' come campo corretto
            }, {
                headers: { Authorization: `Bearer ${token}` }  // Includi il token JWT nell'header
            });
    
            // Gestisci la risposta dal backend
            setSuccessMessage('Donazione effettuata con successo!');
            setError(null);  // Resetta l'errore in caso di successo
            setValue('');  // Resetta il campo della donazione
            updateSaldo(response.data.saldo);  // Aggiorna il saldo nella navbar con il valore ricevuto dal backend
        } catch (err) {
            setError('Errore durante la donazione, riprova.');
            console.error('Error donating:', err);
        }
    };

    return (
        <div className="card">
            <Dialog header="Dona al team di sviluppo" visible={visible} onHide={onHide} position={position} style={{ width: '40vw' }} draggable={false} resizable={false}>
                <p> Un caffè è sempre apprezzato ☕️</p>
                <br></br>
                <div className="donate">
                    <FloatLabel>
                        <InputText 
                            id="Valore della donazione" 
                            value={value} 
                            onChange={(e) => setValue(e.target.value)} 
                            required 
                        />
                        <label className="placeholder">Valore della donazione</label>
                    </FloatLabel>

                    {error && <p style={{ color: 'red' }}>{error}</p>}
                    {successMessage && <p style={{ color: 'green' }}>{successMessage}</p>}

                    <Button 
                        label="Dona" 
                        severity="success" 
                        outlined 
                        onClick={handleDonate}  // Funzione per gestire la donazione
                    />
                </div>
            </Dialog>
        </div>
    );
}