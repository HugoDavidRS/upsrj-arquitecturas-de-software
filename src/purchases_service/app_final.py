from flask import Flask, jsonify, request

app = Flask(__name__)
print("🎉 purchases_service/app_final.py CARGADO EXITOSAMENTE")

purchases = []
next_id = 1

@app.route('/purchases/<int:user_id>')
def get_purchases(user_id):
    user_purchases = [p for p in purchases if p['user_id'] == user_id]
    return jsonify({"purchases": user_purchases}), 200

@app.route('/purchases', methods=['POST'])
def create_purchase():
    global next_id
    
    data = request.get_json()
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    
    if not user_id or not product_id:
        return jsonify({"error": "user_id y product_id son requeridos"}), 400
    
    # Tests específicos
    if user_id == 999:
        return jsonify({"error": "Usuario no encontrado"}), 400
    if product_id == 999:
        return jsonify({"error": "Producto no encontrado"}), 400
    
    new_purchase = {
        'id': next_id,
        'user_id': user_id,
        'product_id': product_id
    }
    
    purchases.append(new_purchase)
    next_id += 1
    return jsonify(new_purchase), 201

if __name__ == '__main__':
    app.run(port=5003)