from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

products = []
next_product_id = 1

@app.route('/products')
def get_products():
    try:
        return render_template('products.html', products=products), 200
    except Exception as e:
        return jsonify({"products": products}), 200

@app.route('/products/<int:product_id>')
def get_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return jsonify(product), 200
    return jsonify({"error": "Producto no encontrado"}), 404

@app.route('/products', methods=['POST'])
def create_product():
    global next_product_id
    
    # Manejar tanto JSON como form-data
    if request.is_json:
        data = request.get_json()
        name = data.get('name') if data else None
        price = data.get('price') if data else None
    else:
        name = request.form.get('name')
        price = request.form.get('price')
    
    if not name or not price:
        return jsonify({"error": "Nombre y precio son requeridos"}), 400
    
    try:
        price = float(price)
    except ValueError:
        return jsonify({"error": "El precio debe ser un número válido"}), 400
    
    new_product = {
        'id': next_product_id,
        'name': name,
        'price': price
    }
    
    products.append(new_product)
    next_product_id += 1
    
    return jsonify(new_product), 200

if __name__ == '__main__':
    app.run(port=5002, debug=True)