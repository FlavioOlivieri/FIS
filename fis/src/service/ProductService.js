import dr from '../assets/dr.jpg';
import el from '../assets/el.jpg';
import gh from '../assets/gh.jpg';
import hl from '../assets/hl.jpg';
import sp from '../assets/sp.jpg';

const ProductService = {
    getProductsSmall() {
        return Promise.resolve([
            {
                productId: 1,
                name: 'Dragon Ball Sparking Zero',
                price: 120,
                image: dr,
                inventoryStatus: 'Disponibilità scarsa',
            },
            {
                productId: 2,
                name: 'Spider-Man 2',
                price: 50,
                image: sp,
                inventoryStatus: 'Disponibilità scarsa',
            },
            {
                productId: 3,
                name: 'Elden Ring',
                price: 70,
                image: el,
                inventoryStatus: 'Disponibilità scarsa',
            },
            {
                productId: 4,
                name: 'Ghost of Tsushima',
                price: 40,
                image: gh,
                inventoryStatus: 'Esaurito',
            },
            {
                productId: 5,
                name: 'Hogwarts Legacy',
                price: 55,
                image: hl,
                inventoryStatus: 'Disponibilità scarsa',
            },
        ]);
    },
};

export { ProductService };