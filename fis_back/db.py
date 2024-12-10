from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
import os
import secrets
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import traceback
from flask_jwt_extended import decode_token, exceptions as jwt_exceptions 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', secrets.token_hex(32))

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    saldo = db.Column(db.Float, nullable=False, default=50)
    products = db.relationship('UserProduct', backref='user', lazy=True)

class Product(db.Model):
    productId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200), nullable=False)
    inventory_status = db.Column(db.String(50), nullable=False)
    user_products = db.relationship('UserProduct', backref='product', lazy=True)

class UserProduct(db.Model):
    __tablename__ = 'user_product'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.productId'), nullable=False)
    acquistato = db.Column(db.Boolean, default=True)  # Indica che l'utente ha acquistato il prodotto

# Inizializzazione del database e popolamento dei prodotti
@app.before_request
def setup_database():
    # Crea tutte le tabelle nel database
    db.create_all()
    
    # Aggiungi i prodotti solo se la tabella è vuota
    if not Product.query.first():
        products = [
            Product(productId=1, name='Dragon Ball Sparking Zero', price=120, image='assets/dr.jpg', inventory_status='Disponibilità scarsa'),
            Product(productId=2, name='Spider-Man 2', price=50, image='assets/sp.jpg', inventory_status='Disponibilità scarsa'),
            Product(productId=3, name='Elden Ring', price=70, image='assets/el.jpg', inventory_status='Disponibilità scarsa'),
            Product(productId=4, name='Ghost of Tsushima', price=40, image='assets/gh.jpg', inventory_status='Esaurito'),
            Product(productId=5, name='Hogwarts Legacy', price=55, image='assets/hl.jpg', inventory_status='Disponibilità scarsa')
        ]
        db.session.bulk_save_objects(products)
        db.session.commit()


# CORS handling
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.route('/status', methods=['GET'])
def status():
    return ("ok")


# Registrazione
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if 'username' not in data or 'email' not in data or 'password' not in data:
            return jsonify({'message': 'Missing fields'}), 400

        # Check if username or email already exists
        existing_user = User.query.filter((User.username == data['username']) | (User.email == data['email'])).first()
        if existing_user:
            return jsonify({'message': 'Username or email already exists'}), 400

        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        user = User(username=data['username'], email=data['email'], password=hashed_password)
        db.session.add(user)
        db.session.commit()

        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error: {str(e)}'}), 400

# Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print('Login data received:', data)  # Log received data
    if 'email' not in data or 'password' not in data:
        return jsonify({'message': 'Missing fields'}), 400

    user = User.query.filter_by(email=data['email']).first()
    if user:
        print('User found:', user)  # Log user found
        if bcrypt.check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity=str(user.id))
            return jsonify({'token': access_token})
        else:
            print('Password check failed')  # Log password check failure
    else:
        print('User not found')  # Log user not found

    return jsonify({'message': 'Invalid credentials'}), 401

# Get user info
@app.route('/user', methods=['GET'])
def user():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"message": "Token mancante o formato non valido"}), 401

    token = auth_header.split(" ")[1]  # Estrarre il token
    print(f"Token ricevuto: {token}")

    try:
        # Decodifica il token manualmente
        decoded_token = decode_token(token)
        print(f"Token decodificato: {decoded_token}")

        # Assicurati che il campo 'sub' sia presente nel payload
        user_id = decoded_token.get('sub')
        if not user_id:
            print("ID utente mancante nel token decodificato.")
            return jsonify({"message": "Token non valido: ID utente mancante"}), 401

        # Cerca l'utente nel database
        user = User.query.get(user_id)
        if not user:
            print(f"Utente con ID {user_id} non trovato.")
            return jsonify({"message": "Utente non trovato"}), 404

        # Risposta con i dati dell'utente
        return jsonify({
            "username": user.username,
            "email": user.email,
            "saldo": user.saldo
        })
    except jwt_exceptions.JWTDecodeError:
        print("Errore: Impossibile decodificare il token.")
        return jsonify({"message": "Token non valido"}), 401
    except Exception as e:
        # Stampa il traceback completo per il debug
        print("Errore imprevisto:", traceback.format_exc())
        return jsonify({"message": "Errore del server"}), 500

#donate
@app.route('/donate', methods=['POST'])
def saldo():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"message": "Token mancante o formato non valido"}), 401

    token = auth_header.split(" ")[1]  # Estrarre il token
    print(f"Token ricevuto: {token}")

    try:
        # Decodifica il token manualmente
        decoded_token = decode_token(token)
        print(f"Token decodificato: {decoded_token}")

        # Assicurati che il campo 'sub' sia presente nel payload
        user_id = decoded_token.get('sub')
        if not user_id:
            print("ID utente mancante nel token decodificato.")
            return jsonify({"message": "Token non valido: ID utente mancante"}), 401

        # Cerca l'utente nel database
        user = User.query.get(user_id)
        if not user:
            print(f"Utente con ID {user_id} non trovato.")
            return jsonify({"message": "Utente non trovato"}), 404

        # Ottieni i dati della richiesta
        data = request.get_json()
        if 'amount' not in data:
            return jsonify({'message': 'Missing fields'}), 410

        # Aggiorna il saldo dell'utente
        if data['amount'] < 0:
            user.saldo += abs(data['amount'])
        else:
            if user.saldo - data['amount'] < 0:
                return jsonify({'message': 'Insufficient balance'}), 400
            user.saldo -= data['amount']

        # Salva le modifiche nel database
        db.session.commit()
        return jsonify({'saldo': user.saldo})
    except jwt_exceptions.JWTDecodeError:
        print("Errore: Impossibile decodificare il token.")
        return jsonify({"message": "Token non valido"}), 401
    except Exception as e:
        # Stampa il traceback completo per il debug
        print("Errore imprevisto:", traceback.format_exc())
        return jsonify({"message": "Errore del server"}), 500


@app.route('/products', methods=['GET'])
def get_products():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"message": "Token mancante o formato non valido"}), 401

    token = auth_header.split(" ")[1]  # Estrarre il token
    print(f"Token ricevuto: {token}")

    try:
        # Decodifica del token
        decoded_token = decode_token(token)
        print(f"Token decodificato: {decoded_token}")

        # Verifica che il token contenga il campo 'sub'
        user_id = decoded_token.get('sub')
        if not user_id:
            print("ID utente mancante nel token decodificato.")
            return jsonify({"message": "Token non valido: ID utente mancante"}), 401

        # Cerca l'utente nel database
        user = User.query.get(user_id)
        if not user:
            print(f"Utente con ID {user_id} non trovato.")
            return jsonify({"message": "Utente non trovato"}), 404

        # Recupera i prodotti dal database
        products = Product.query.all()

        # Formatta i prodotti in un dizionario JSON
        products_list = [{
            'productId': product.productId,
            'name': product.name,
            'price': product.price,
            'image': product.image,
            'inventoryStatus': product.inventory_status,
            # Include l'elenco di utenti associati se necessario
            'userProducts': [
                {'userId': user_product.user_id} for user_product in product.user_products
            ] if product.user_products else []
        } for product in products]

        # Risponde con i prodotti
        return jsonify(products_list), 200

    except jwt_exceptions.JWTDecodeError:
        print("Errore: Impossibile decodificare il token.")
        return jsonify({"message": "Token non valido"}), 401
    except Exception as e:
        # Log dell'errore e risposta generica
        print("Errore imprevisto:", traceback.format_exc())
        return jsonify({'message': f'Error: {str(e)}'}), 500



@app.route('/buy', methods=['POST'])
def buy():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"message": "Token mancante o formato non valido"}), 401

    token = auth_header.split(" ")[1]  # Estrarre il token
    print(f"Token ricevuto: {token}")

    try:
        # Decodifica il token manualmente
        decoded_token = decode_token(token)
        print(f"Token decodificato: {decoded_token}")

        # Assicurati che il campo 'sub' sia presente nel payload
        user_id = decoded_token.get('sub')
        if not user_id:
            print("ID utente mancante nel token decodificato.")
            return jsonify({"message": "Token non valido: ID utente mancante"}), 401

        # Cerca l'utente nel database
        user = User.query.get(user_id)
        if not user:
            print(f"Utente con ID {user_id} non trovato.")
            return jsonify({"message": "Utente non trovato"}), 404

        # Ottieni i dati della richiesta
        data = request.get_json()
        if 'id' not in data:
            return jsonify({'message': 'Product ID missing'}), 400

        product_id = data['id']
        product = Product.query.get(product_id)

        if not product:
            return jsonify({'message': 'Product not found'}), 404

        # Verifica se l'utente ha già acquistato il prodotto
        user_product = UserProduct.query.filter_by(user_id=user.id, product_id=product_id).first()
        if user_product:
            return jsonify({'message': 'Product already purchased by the user'}), 400

        # Verifica il saldo
        if user.saldo - product.price < 0:
            return jsonify({'message': 'Insufficient balance'}), 400

        # Aggiorna saldo e registra l'acquisto
        user.saldo -= product.price
        new_user_product = UserProduct(user_id=user.id, product_id=product_id)
        db.session.add(new_user_product)
        db.session.commit()

        return jsonify({'saldo': user.saldo, 'message': 'Purchase successful'})

    except jwt_exceptions.JWTDecodeError:
        print("Errore: Impossibile decodificare il token.")
        return jsonify({"message": "Token non valido"}), 401
    except Exception as e:
        # Ripristina il database in caso di errore
        db.session.rollback()
        print("Errore imprevisto:", traceback.format_exc())
        return jsonify({'message': f'Error: {str(e)}'}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
