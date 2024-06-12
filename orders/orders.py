# order_management.py
from flask import Flask, request, jsonify
from flask_restful import Api
from flask import Response
from pymongo import MongoClient
import json
from datetime import datetime, timezone

app = Flask(__name__)
api = Api(app)


client = MongoClient('mongodb://mongodb-service:27017/')
db = client['ecommerce']
orders_collection = db['orders']
logged_in_collection = db['logged_in']

@app.route('/post_order', methods=['POST'])
def post_order():
    user_name = request.args.get('user_name')
    product_name = request.args.get('product_name')
    size = request.args.get('size')
    quantity = request.args.get('quantity')
    
    # Add the user_name and current timestamp to the products collection
    orders_collection.insert_one({
        'product_name': product_name,
        'user_name': user_name,
        'size': size,
        'quantity': quantity,
        'timestamp': str(datetime.now(timezone.utc))
    })
    return jsonify({'message': 'Order logged successfully'}), 201

@app.route('/orders', methods=['GET'])
def get_orders():
    user = logged_in_collection.find_one()
    username = user.get('user_name')
    if username:
        orders = list(orders_collection.find({'user_name': username}, {'_id': 0, 'user_name': 0}))
        formatted_orders = '\n'.join([str(order) for order in orders])
        response_text = f"Orders of {username}:\n{formatted_orders}"
        return jsonify(response_text), 201
    else:
        return jsonify({'error': 'No user logged in'}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True, threaded=True)
