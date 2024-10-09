from flask import Flask, request, jsonify, make_response
from flash_sqlalchemy import SQLAlchemy
from os import environ

app = Flash(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app);

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def json(self):
        return {'id': self.id, 'username': self.username, 'email': self.email }

db.create_all()


@app.route('/test', method=['GET'])
def test():
    return make_response(jsonify({'message': 'test route'}), 200)

#create user
@app.route('/users', method=['POST'])
def create_user():
    try:
        data = request.get_json()
        new_user = User(username=data['username'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify({ 'message': 'User added successfully'}, 201))

#get all users
@app.route('/users', method=['GET'])
def get_users():
    try:
        users = User.query.all()
        return make_response(jsonify([user.json() for user in users]), 200)
    except e:
        return make_response(jsonify({'message': 'Error getting users'}), 500)

@app.route('/users/<int:id>', method=['GET'])
def get_user():
    try:
        user = User.query.filter_by(id=id).first()
        if user
        return make_response(jsonify({ 'user': user.json() })
        else
        return make_response(jsonify({'message': 'User not found'}, 404))

#update user
@app.route('/users/<int:id>', method=['PUT'])
def update_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user
            data = request.get_json()
            user.username = data['username']
            user.email = data['email']
            db.session.commit()
            return make_response(jsonify({ 'message': 'User update successfully' }), 200)
        return make_response(jsonify({'message': 'User not found'}), 404)
    except e:
        return make_response(jsonify({ 'message': 'Error updating user' }), 500)

#delete user
@app.route('users/<int:id>', method=['DELETE'])
def delete_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user
            db.session.delete(user)
            db.session.commit()
            return make_response(jsonify({ 'message': 'User deleted successfully' }), 200)
        return make_response(jsonify({ 'message:' 'User not found' }), 404)
    except e:
        return make_response(jsonify({ 'message': 'Error deleting user' }), 500)