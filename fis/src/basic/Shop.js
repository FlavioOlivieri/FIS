import React, { useState, useEffect } from 'react';
import { Button } from 'primereact/button';
import { Carousel } from 'primereact/carousel';
import { Tag } from 'primereact/tag';
import axios from 'axios';
import '../css/Shop.css';

export default function Shop({ visible, onHide, updateSaldo }) {
    const [products, setProducts] = useState([]);
    const [saldo, setSaldo] = useState(null);

    const getSeverity = (product) => {
        switch (product.inventoryStatus) {
            case 'Disponibilità ottima':
                return 'success';
            case 'Disponibilità scarsa':
                return 'warning';
            case 'Esaurito':
                return 'danger';
            default:
                return null;
        }
    };

    useEffect(() => {
        const fetchProducts = async () => {
            const token = localStorage.getItem('token');
            try {
                const response = await axios.get('http://localhost:5001/products', {
                    headers: { Authorization: `Bearer ${token}` }
                });
                setProducts(response.data);
            } catch (error) {
                console.error("Errore nel recupero dei prodotti:", error);
            }
        };

        const fetchSaldo = async () => {
            const token = localStorage.getItem('token');
            try {
                const response = await axios.get('http://localhost:5001/user', {
                    headers: { Authorization: `Bearer ${token}` }
                });
                setSaldo(response.data.saldo);
            } catch (error) {
                console.error("Errore nel recupero del saldo:", error);
            }
        };

        fetchProducts();
        fetchSaldo();
    }, []);

    const handleBuy = async (productId) => {
        const token = localStorage.getItem('token');
        console.log(`Attempting to buy product with ID: ${productId}`);

        try {
            const response = await axios.post('http://localhost:5001/buy', { id: productId }, {
                headers: { Authorization: `Bearer ${token}` }
            });

            if (response && response.data && response.data.message === 'Purchase successful') {
                setSaldo(response.data.saldo);
                updateSaldo(response.data.saldo);
                setProducts((prevProducts) =>
                    prevProducts.map((product) =>
                        product.productId === productId
                            ? { ...product, inventoryStatus: 'Esaurito', acquistato: true }
                            : product
                    )
                );
            } else {
                alert(response.data ? response.data.message : 'Error: No response data');
            }
        } catch (error) {
            console.error('Error during purchase:', error);
            if (error.response && error.response.data) {
                alert(error.response.data.message || 'Errore durante l\'acquisto. Riprova.');
            } else {
                alert('Errore durante l\'acquisto. Nessuna risposta dal server.');
            }
        }
    };

    const productTemplate = (product) => {
        const isProductOutOfStock = product.inventoryStatus === 'Esaurito';
        return (
            <div>
                <div className='imgProduct'>
                    <img src={`http://localhost:5001/static/${product.image}`} alt={product.name} />
                </div>
                <div className='detailsProduct'>
                    <h2>{product.name}</h2>
                    <h4>{product.price.toFixed(2)} €</h4>
                    <Tag value={product.inventoryStatus} severity={getSeverity(product)}></Tag>
                    <div>
                        {isProductOutOfStock && product.acquistato ? (
                            <Button label="Acquistato" className="p-button-success p-button-rounded" disabled />
                        ) : isProductOutOfStock ? (
                            <Button label="Non acquistabile" className="p-button-danger p-button-rounded" disabled />
                        ) : (
                            <Button 
                                icon="pi pi-shopping-bag" 
                                className="p-button p-button-rounded" 
                                label="Acquista"
                                onClick={() => handleBuy(product.productId)} 
                            />
                        )}
                    </div>
                </div>
            </div>
        );
    };

    return (
        <div className="carousel-container">
            <Carousel value={products} numVisible={1} numScroll={1} orientation="vertical" verticalViewPortHeight="30rem"
            itemTemplate={productTemplate} />
        </div>
    );
}