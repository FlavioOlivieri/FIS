import React, { useEffect, useState } from 'react'; 
import { Fieldset } from 'primereact/fieldset';
import { Avatar } from 'primereact/avatar';
import flavio from '../assets/Flavio.png';
import '../css/Info.css';

export default function Info_Flavio({ visible, onHide }) {
    const [fadeClass, setFadeClass] = useState('fade-out');

    useEffect(() => {
        if (visible) {
            setFadeClass('fade-in');
        } else {
            setFadeClass('fade-out');
        }
    }, [visible]);

    const legendTemplate = (
        <div className='box'>
            <Avatar className="avatar" image={flavio} shape="circle" />
            <span className="font-bold">Flavio Olivieri</span>
        </div>
    );

    return (
        <div className={`card ${fadeClass}`} onAnimationEnd={onHide}>
            <Fieldset legend={legendTemplate}>
                <p className="m-0">
                    Sono Flavio Olivieri. Sono laureato in Ingegneria Informatica e dell'Automazione presso il Politecnico di Bari. La mia tesi si è
                    concentrata sulle BCI e sull'analisi dei segnali P300 con la creazione di un Oddball Test. <br />
                    Attualmente sto frequentando la laurea magistrale in Ingegneria delle Telecomunicazioni curriculum Cyber Security sempre presso il 
                    Politecnico di Bari.
                </p>
            </Fieldset>
        </div>
    );
}