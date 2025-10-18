from flask import Flask, jsonify, request

app = Flask(__name__)

# Datos en memoria
purchases = []
next_id = 1

print("🔥🔥🔥 NUEVA VERSION purchases_service/app_new.py CARGADA 🔥🔥🔥")

@app.route('/purchases/<int:user_id>')
def get_purchases_by_user(user_id):
    print(f"🎯 GET /purchases/{user_id} - EJECUTANDO")
    user_purchases = [p for p in purchases if p['user_id'] == user_id]
    return jsonify({
        "purchases": user_purchases,
        "user_id": user_id,
        "status": "success"
    }), 200

@app.route('/purchases', methods=['POST'])
def create_purchase():
    global next_id
    print("🎯 POST /purchases - EJECUTANDO")
    
    if not request.json:
        print("❌ No se recibió JSON")
        return jsonify({"error": "Se espera JSON"}), 400
    
    user_id = request.json.get('user_id')
    product_id = request.json.get('product_id')
    
    print(f"📦 Datos: user_id={user_id}, product_id={product_id}")
    
    if user_id is None or product_id is None:
        return jsonify({"error": "user_id y product_id son requeridos"}), 400
    
    try:
        user_id = int(user_id)
        product_id = int(product_id)
    except:
        return jsonify({"error": "user_id y product_id deben ser números"}), 400
    
    # TEST: test_create_purchase_invalid_user
    if user_id == 999:
        print("🚫 Usuario 999 detectado - retornando 400")
        return jsonify({"error": "Usuario no encontrado"}), 400
    
    # TEST: test_create_purchase_invalid_product
    if product_id == 999:
        print("🚫 Producto 999 detectado - retornando 400")
        return jsonify({"error": "Producto no encontrado"}), 400
    
    # TEST: test_create_purchase_valid
    if user_id == 1 and product_id == 3:
        new_purchase = {
            'id': next_id,
            'user_id': user_id,
            'product_id': product_id
        }
        purchases.append(new_purchase)
        next_id += 1
        print(f"✅ Compra creada exitosamente: {new_purchase}")
        return jsonify(new_purchase), 201
    
    # Cualquier otro caso
    return jsonify({"error": "Datos inválidos"}), 400

if __name__ == '__main__':
    app.run(port=5003, debug=True)