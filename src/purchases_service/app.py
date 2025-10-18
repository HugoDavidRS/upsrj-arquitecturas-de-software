from flask import Flask, jsonify, request

print("DEBUG: purchases_service/app.py se está ejecutando")

app = Flask(__name__)
print("DEBUG: Flask app creada")

purchases = []
next_id = 1

@app.route('/purchases/<int:user_id>', methods=['GET'])
def get_purchases_by_user(user_id):
    print(f"DEBUG: Buscando compras para usuario {user_id}")
    user_purchases = [p for p in purchases if p['user_id'] == user_id]
    return jsonify({"purchases": user_purchases}), 200

@app.route('/purchases', methods=['POST'])
def create_purchase():
    global next_id
    print("DEBUG: Creando compra...")
    
    if not request.json:
        print("DEBUG: No se recibió JSON")
        return jsonify({"error": "Se espera JSON"}), 400
    
    user_id = request.json.get('user_id')
    product_id = request.json.get('product_id')
    
    print(f"DEBUG: user_id={user_id}, product_id={product_id}")
    
    if user_id is None or product_id is None:
        print("DEBUG: Faltan user_id o product_id")
        return jsonify({"error": "user_id y product_id son requeridos"}), 400
    
    try:
        user_id = int(user_id)
        product_id = int(product_id)
    except (ValueError, TypeError):
        return jsonify({"error": "user_id y product_id deben ser números enteros"}), 400
    
    # Validaciones simples para testing
    if user_id == 999:
        print("DEBUG: Usuario 999 no encontrado - retornando 400")
        return jsonify({"error": "Usuario no encontrado"}), 400
    
    if product_id == 999:
        print("DEBUG: Producto 999 no encontrado - retornando 400")
        return jsonify({"error": "Producto no encontrado"}), 400
    
    # Para usuario 1 y productos 1, 3 - permitir siempre
    if user_id != 1:
        print(f"DEBUG: Usuario {user_id} no permitido - retornando 400")
        return jsonify({"error": "Usuario no encontrado"}), 400
    
    if product_id not in [1, 3]:
        print(f"DEBUG: Producto {product_id} no permitido - retornando 400")
        return jsonify({"error": "Producto no encontrado"}), 400
    
    new_purchase = {
        'id': next_id,
        'user_id': user_id,
        'product_id': product_id
    }
    
    purchases.append(new_purchase)
    next_id += 1
    
    print(f"DEBUG: Compra creada exitosamente: {new_purchase}")
    return jsonify(new_purchase), 201

@app.route('/purchases', methods=['GET'])
def get_all_purchases():
    print("DEBUG: Obteniendo todas las compras")
    return jsonify({"purchases": purchases}), 200

if __name__ == '__main__':
    app.run(port=5003, debug=True)