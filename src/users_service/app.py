from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

users = []
next_user_id = 1

@app.route('/users')
def get_users():
    try:
        return render_template('users.html', users=users), 200
    except Exception as e:
        return jsonify({"users": users}), 200

@app.route('/users/<int:user_id>')
def get_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        return jsonify(user), 200
    return jsonify({"error": "Usuario no encontrado"}), 404

@app.route('/users', methods=['POST'])
def create_user():
    global next_user_id
    
    # Manejar tanto JSON como form-data
    if request.is_json:
        data = request.get_json()
        name = data.get('name') if data else None
    else:
        name = request.form.get('name')
    
    if not name:
        return jsonify({"error": "El nombre es requerido"}), 400
    
    new_user = {
        'id': next_user_id,
        'name': name
    }
    
    users.append(new_user)
    next_user_id += 1
    
    return jsonify(new_user), 200

if __name__ == '__main__':
    app.run(port=5001, debug=True)