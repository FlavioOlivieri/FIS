import React, { useEffect, useState }  from 'react'; 
import { Fieldset } from 'primereact/fieldset';
import { Avatar } from 'primereact/avatar';
import miki from '../assets/Miki.png';
import '../css/Info.css';

export default function Info_Miki({visible, onHide}) {
    const [fadeClass, setFadeClass] = useState('fade-out');

    useEffect(() => {
        if (visible) {
            setFadeClass('fade-in');
        } else {
            setFadeClass('fade-out');
        }
    }, [visible]);

    const legendTemplate = (
        <div className="flex align-items-center gap-2 px-2">
            <Avatar className="avatar" image={miki} shape="circle" />
            <span className="font-bold">Miki Palmisano</span>
        </div>
    );

    return (
        <div className={`card ${fadeClass}`} onAnimationEnd={onHide}>
            <Fieldset legend={legendTemplate}>
                <p className="m-0">
                    Sono Miki Palmisano. Sono laureato in Ingegneria Informatica e dell'Automazione presso il Politecnico di Bari. La mia tesi si è
                    concentrata sull'Intelligenza Artificiale e le possibili implicazioni e pericoli che può avere con il mondo. <br />
                    Attualmente sto frequentando la laurea magistrale in Ingegneria Informatica curriculum AI e Data Science sempre presso il 
                    Politecnico di Bari.
                </p>
            </Fieldset>
        </div>
    )
}
        