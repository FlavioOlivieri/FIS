import React, { useState, useEffect } from 'react';
import { Menubar } from 'primereact/menubar';
import fis from '../assets/fis.png';
import majorana from '../assets/majorana.png';
import '../css/navbar.css';
import Info_Flavio from './Info_Flavio';
import Info_Miki from './Info_Miki';
import Donate from './Donate';
import Shop from './Shop';
import { Card } from 'primereact/card';
import axios from 'axios';

const API_URL = 'http://192.168.1.9:5001'; 

export default function Navbar() {
    const [dialogVisible, setDialogVisible] = useState(true);
    const [dialogType, setDialogType] = useState("shop");
    const [username, setUsername] = useState('');
    const [saldo, setSaldo] = useState(0.0);

    // Funzione per recuperare le informazioni utente, incluso il saldo
    const fetchUserInfo = async () => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.get(`${API_URL}/user`, {
                headers: { Authorization: `Bearer ${token}` }
            });
            setUsername(response.data.username);
            setSaldo(response.data.saldo);
        } catch (error) {
            console.error('Error fetching user info:', error);
        }
    };

    useEffect(() => {
        fetchUserInfo();
    }, []);

    // Funzione che aggiorna il saldo
    const updateSaldo = (newSaldo) => {
        setSaldo(newSaldo);
    };

    const items = [
        {
            label: 'Negozio',
            icon: 'pi pi-shop',
            command: () => {
                setDialogType("shop");
                setDialogVisible(true);
            }
        },
        {
            label: 'Donazione',
            icon: 'pi pi-dollar',
            command: () => {
                setDialogType("donate");
                setDialogVisible(true);
            }
        },
        {
            label: 'Info',
            icon: 'pi pi-info-circle',
            command: () => {
                setDialogType("info");
                setDialogVisible(true);
            }
        },
        {
            label: 'Logout',
            icon: 'pi pi-sign-out',
            command: () => {
                localStorage.removeItem('token');
                window.location.reload();
            }
        }
    ];

    const start = <img alt="logo" src={fis} height="50" className="mr-2"></img>;
    const end =
        <div className="endNav">
            <Card className="saldo" title={`Saldo di ${username}:`}>
                <p> {saldo.toFixed(2)} €</p>
            </Card>
            <img alt="logo" src={majorana} height="60" className="mr-2"></img>
        </div>;

    return (
        <div className="card">
            <Menubar model={items} start={start} end={end} />

            {dialogVisible && dialogType === "info" && (
                <>
                    <Info_Flavio
                        visible={dialogVisible}
                        onHide={() => setDialogVisible(false)}
                    />
                    <Info_Miki
                        visible={dialogVisible}
                        onHide={() => setDialogVisible(false)}
                    />
                </>
            )}

            {dialogVisible && dialogType === "donate" && (
                <Donate
                    visible={dialogVisible}
                    onHide={() => {
                        setDialogVisible(false);
                        setDialogType("shop"); // Quando si chiude il dialogo "donate", riapre lo shop
                        setTimeout(() => setDialogVisible(true), 100); // Riapre dopo un breve ritardo
                    }}
                    updateSaldo={updateSaldo}  // Passiamo la funzione per aggiornare il saldo
                />
            )}

            {dialogVisible && dialogType === "shop" && (
                <Shop
                    visible={dialogVisible}
                    onHide={() => setDialogVisible(false)}
                    updateSaldo={updateSaldo}  // Passiamo la funzione per aggiornare il saldo
                />
            )}
        </div>
    );
}
