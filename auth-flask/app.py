from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import datetime
import jwt
from functools import wraps

# instacia os metodos
db = SQLAlchemy()
app = Flask(__name__)

# configura a secret key e o caminho do banco de dados
app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'

# inicializa o banco de dados
db.init_app(app)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50))
    name = db.Column(db.String(50))
    age = db.Column(db.String(2))
    password = db.Column(db.String(80))


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "Authentication" in request.headers:
            token =  request.headers["Authentication"]
            
        
        if not token:
            return jsonify({'message': 'nao existe token'}),401
        
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            
            
        except jwt.InvalidTokenError:
            return jsonify({'message': 'token e invalido'}), 403
        
        return f( *args, **kwargs)

    return decorated


@app.route('/user', methods=['GET'])
@token_required
def todos_usuarios():
    
    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['age'] = user.age
        user_data['email'] = user.email
        output.append(user_data)
    
    return jsonify({'users': output})

@app.route('/user/<public_id>', methods=['GET'])
@token_required
def um_usuario(public_id):
    
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'User not found!'})
    

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['age'] = user.age
    user_data['email'] = user.email



    return jsonify({'user': user_data})
    


@app.route('/user', methods=['POST'])
def criar_usuario():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()), name=data['name'],email=data['email'], age=data['age'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New user created!'})


@app.route('/user/<public_id>', methods=['PUT'])
@token_required
def atualizar_usuario(public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'User not found!'})

    user.email = request.json['email']
    user.name = request.json['name']

    db.session.commit()

    return jsonify({'message': 'name or email has been changed!'})


@app.route('/user/<public_id>', methods=['DELETE'])
@token_required
def deletar_usuario(public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'User not found!'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message':'User deleted!'})
    

@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Nao pode verificar',401,{'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = User.query.filter_by(name=auth.username).first()

    if not user:
        return make_response('Nao pode verificar',401,{'WWW-Authenticate' : 'Basic realm="Login required!"'})
    
    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token': token})
    return make_response('Nao pode verificar2',401,{'WWW-Authenticate' : 'Basic realm="Login required!"'})

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)