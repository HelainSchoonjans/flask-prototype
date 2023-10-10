from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

# Initialize the JWT manager
jwt = JWTManager()

# Mock user data for demonstration
users = {
    'username': 'password'
}

def create_app():
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
    jwt.init_app(app)

    @app.route('/')
    def hello():
        return 'Hello, World!'

    @app.route('/login', methods=['POST'])
    def login():
        username = request.json.get('username', None)
        password = request.json.get('password', None)

        if username not in users or users[username] != password:
            return jsonify({'message': 'Invalid credentials'}), 401

        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200

    @app.route('/protected', methods=['GET'])
    @jwt_required()
    def protected():
        current_user = 'example_user'  # This can be retrieved from the JWT token
        return jsonify(logged_in_as=current_user), 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)