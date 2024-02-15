from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_httpauth import HTTPBasicAuth
import uuid
from sqlalchemy import text
from datetime import datetime
from flask import current_app

app = Flask(__name__)
auth = HTTPBasicAuth()

# database configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/Users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(36), primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    account_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    account_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

@auth.verify_password
def verify_password(username, password):
    current_app.logger.debug(f"Authenticating user: {username}")
    current_app.logger.debug(f"Authenticating password: {password}")
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        return username

@app.route('/v1/user', methods=['POST'])
def create_user():
    data = request.json
    username = data['username']
    print()
    if request.args:
        return make_response('', 400, {'Cache-Control': 'no-cache'})

    if User.query.filter_by(username=username).first():
        return make_response(jsonify({"error": "User already exists"}), 400, {'Cache-Control': 'no-cache'})
    
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(
        id=str(uuid.uuid4()),
        first_name=data['first_name'],
        last_name=data['last_name'],
        username=username,
        password=hashed_password
    )
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "account_created": user.account_created.isoformat() + 'Z',
        "account_updated": user.account_updated.isoformat() + 'Z'
    }), 201


@app.route('/v1/user/self', methods=['PUT'])
@auth.login_required
def update_user():
    data = request.json
    username = auth.current_user()
    user = User.query.filter_by(username=username).first()
    if request.args:
        return make_response('', 400, {'Cache-Control': 'no-cache'})

    if not user:
        return make_response(jsonify({"error": "User not found"}), 404, {'Cache-Control': 'no-cache'})
    
    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']
    if 'password' in data:
        user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    else:
        return make_response(jsonify({"error": "Bad Request. Missing required fields."}), 400, {'Cache-Control': 'no-cache'})

    user.account_updated = datetime.utcnow()
    db.session.commit()
    
    return '', 204



@app.route('/v1/user/self', methods=['GET'])
@auth.login_required
def get_user():
    username = auth.current_user()
    user = User.query.filter_by(username=username).first()
    # check for query params
    if request.args:
        return make_response('', 503, {'Cache-Control': 'no-cache'})

    if user:
        user_data = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "account_created": user.account_created.isoformat() + 'Z',
            "account_updated": user.account_updated.isoformat() + 'Z'
        }
        return jsonify(user_data), 200
    else:
        return make_response(jsonify({"error": "User not found"}), 404, {'Cache-Control': 'no-cache'})

# Public end points: Operations available to all users without authentication 
@app.route('/healthz', methods=['GET'])
def health_end_point():
    # check for query params
    if request.args:
        return make_response('', 503, {'Cache-Control': 'no-cache'})
    # check if payload (payload not allowed)
    if request.get_data():
        return make_response('', 503, {'Cache-Control': 'no-cache'})

    try:
        # check connection with database
        db.session.execute(text('SELECT * from user'))
        db.session.commit()
        return make_response('', 200, {'Cache-Control': 'no-cache'})

    except Exception as e:
        return make_response('', 503, {'Cache-Control': 'no-cache'})
   
@app.route('/healthz', methods=['POST'])   
def health_post_end_point():
    return make_response('', 405, {'Cache-Control': 'no-cache'})

@app.route('/healthz', methods=['PUT'])   
def health_put_end_point():
    return make_response('', 405, {'Cache-Control': 'no-cache'})

@app.route('/healthz', methods=['DELETE'])   
def health_delete_end_point():
    return make_response('', 405, {'Cache-Control': 'no-cache'})

@app.route('/healthz', methods=['HEAD'])   
def health_head_end_point():
    return make_response('', 405, {'Cache-Control': 'no-cache'})

@app.route('/healthz', methods=['OPTIONS'])   
def health_options_end_point():
    return make_response('', 405, {'Cache-Control': 'no-cache'})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port= 8080, debug=True)
