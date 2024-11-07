from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
import os
import secrets

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', secrets.token_hex(32))

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Model per gli utenti
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    saldo = db.Column(db.Float, nullable=False, default=50)

# Model per i prodotti
class Product(db.Model):
    productId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200), nullable=False)
    inventory_status = db.Column(db.String(50), nullable=False)
    acquistato = db.Column(db.Boolean, default=False) 

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
            access_token = create_access_token(identity=user.id)
            return jsonify({'token': access_token})
        else:
            print('Password check failed')  # Log password check failure
    else:
        print('User not found')  # Log user not found

    return jsonify({'message': 'Invalid credentials'}), 401

# Get user info
@app.route('/user', methods=['GET'])
@jwt_required()
def user():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    print(f"Current user: {user}")
    return jsonify({'username': user.username, 'email': user.email, 'saldo': user.saldo})

#donate
@app.route('/donate', methods=['POST'])
@jwt_required()
def saldo():
    data = request.get_json()
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if 'amount' not in data:
        return jsonify({'message': 'Missing fields'}), 400
    
    if data['amount'] < 0:
        user.saldo += abs(data['amount'])
    else:
        if user.saldo - data['amount'] < 0:
            return jsonify({'message': 'Insufficient balance'}), 400
        user.saldo -= data['amount']

    db.session.commit()
    return jsonify({'saldo': user.saldo})

@app.route('/products', methods=['GET'])
@jwt_required()
def get_products():
    try:
        products = Product.query.all()
        products_list = [{
            'productId': product.productId,
            'name': product.name,
            'price': product.price,
            'image': product.image,
            'inventoryStatus': product.inventory_status,
            'acquistato': product.acquistato
        } for product in products]
        return jsonify(products_list)
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': f'Error: {str(e)}'}), 500

@app.route('/buy', methods=['POST'])
@jwt_required()
def buy():
    try:
        data = request.get_json()
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if 'id' not in data:
            return jsonify({'message': 'Product ID missing'}), 400

        product_id = data['id']
        product = Product.query.get(product_id)

        if not product:
            return jsonify({'message': 'Product not found'}), 404

        if product.inventory_status.lower() == 'esaurito' or product.acquistato:
            return jsonify({'message': 'Product out of stock or already purchased'}), 400

        if user.saldo - product.price < 0:
            return jsonify({'message': 'Insufficient balance'}), 400

        user.saldo -= product.price
        product.inventory_status = 'Esaurito'
        product.acquistato = True 

        db.session.commit()
        return jsonify({'saldo': user.saldo, 'message': 'Purchase successful'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)
