from flask import Flask, request, jsonify

app = Flask(__name__)

# Datos en memoria
purchases = []
next_purchase_id = 1

# Usuarios y productos existentes para testing
existing_users = {1: True}
existing_products = {1: True, 3: True}

@app.route('/purchases/<int:user_id>', methods=['GET'])
def get_purchases_by_user(user_id):
    print(f"DEBUG: Buscando compras para usuario {user_id}")
    user_purchases = [p for p in purchases if p['user_id'] == user_id]
    return jsonify({
        "user_id": user_id,
        "purchases": user_purchases,
        "message": "Compras del usuario"
    }), 200

@app.route('/purchases', methods=['GET'])
def get_all_purchases():
    return jsonify({
        "purchases": purchases,
        "count": len(purchases)
    }), 200

@app.route('/purchases', methods=['POST'])
def create_purchase():
    global next_purchase_id
    
    print("DEBUG: Creando compra...")
    
    if not request.is_json:
        return jsonify({"error": "Se espera JSON"}), 400
    
    data = request.get_json()
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    
    print(f"DEBUG: user_id={user_id}, product_id={product_id}")
    
    if user_id is None or product_id is None:
        return jsonify({"error": "user_id y product_id son requeridos"}), 400
    
    try:
        user_id = int(user_id)
        product_id = int(product_id)
    except (ValueError, TypeError):
        return jsonify({"error": "user_id y product_id deben ser números enteros"}), 400
    
    # Verificar usuario
    if user_id not in existing_users:
        print(f"DEBUG: Usuario {user_id} no encontrado")
        return jsonify({"error": "Usuario no encontrado"}), 400
    
    # Verificar producto
    if product_id not in existing_products:
        print(f"DEBUG: Producto {product_id} no encontrado")
        return jsonify({"error": "Producto no encontrado"}), 400
    
    new_purchase = {
        'id': next_purchase_id,
        'user_id': user_id,
        'product_id': product_id
    }
    
    purchases.append(new_purchase)
    next_purchase_id += 1
    
    print(f"DEBUG: Compra creada: {new_purchase}")
    return jsonify(new_purchase), 201

if __name__ == '__main__':
    app.run(port=5003, debug=True)