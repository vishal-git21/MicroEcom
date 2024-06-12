from flask import Flask, request, jsonify, render_template
from flask_restful import Api
import json
import requests
from pymongo import MongoClient
from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key' 
client = MongoClient('mongodb://mongodb-service:27017/')

api = Api(app)

# Custom decorator to check if the user is authenticated
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_authenticated' not in session:
            return redirect('/login')  # Redirect to login page if not authenticated
        return f(*args, **kwargs)
    return decorated_function

# URL of the services 
USERS_URL = 'http://users-service:5004'
PRODUCTS_URL = 'http://products-service:5002'
ORDERS_URL = 'http://orders-service:5005'

@app.route('/add_user')
def add_user():
    user_name = request.args.get('user_name')
    password = request.args.get('password')
    age = request.args.get('age')
    country = request.args.get('country')
    gender = request.args.get('gender')
    response = requests.post(f"{USERS_URL}/add_user?user_name={user_name}&password={password}&age={age}&country={country}&gender={gender}")
    if response.status_code == 201:
        requests.post(f"{USERS_URL}/auth_user?user_name={user_name}")
        return redirect('/home')
    else:
        return redirect('/login')
    
@app.route('/fetch_user')
def fetch_user():
    user_name = request.args.get('user_name')
    password = request.args.get('password')
    response = requests.get(f"{USERS_URL}/fetch_user?user_name={user_name}&password={password}")
    if response.status_code == 201:
        requests.post(f"{USERS_URL}/auth_user?user_name={user_name}")
        return redirect('/home')
    else:
       return redirect('/login')


@app.route('/user_order', methods=['POST'])
def user_order():
    data = request.json
    response = requests.post(f"{USERS_URL}/user_order", json=data)
    return response.json()



@app.route('/auth_user', methods=['POST'])
def auth_user():
    user_name = request.args.get('user_name')
    response = requests.post(f"{USERS_URL}/auth_user?user_name={user_name}")
    # if response.status_code == 201:
    #     session['user_authenticated'] = True
    return response.json(), response.status_code

@app.route('/logout')
def logout_user():
    response = requests.post(f"{USERS_URL}/logout")
    requests.post(f"{PRODUCTS_URL}/clear_current_product")
    return response.json(), response.status_code

@app.route('/authed_user', methods=['GET'])
def authed_user():
    response = requests.get(f"{USERS_URL}/authed_user")
    return response.json()

@app.route('/orders')
def orders():
    response = requests.get(f"{ORDERS_URL}/orders")
    if response.status_code == 201:
        return jsonify(response.json()), 201
    else:
        return jsonify({"error": "Failed to fetch orders"}), response.status_code

@app.route('/products')
def products():
    response = requests.get(f"{PRODUCTS_URL}/products")
    return response.json()

@app.route('/login')
def landing_page():
    # if session['user_authenticated'] == True:
    #     return redirect('/home')
    return render_template('landing_page.html')

@app.route('/home')
def home_page():
    response = requests.get(f"{USERS_URL}/authed_user")
    user_name = response.json().get('user_name')
    return render_template('index.html', user_name=user_name)

@app.route('/checkout')
def checkout_page():
    product_name = request.args.get('product_name')
    requests.post(f"{PRODUCTS_URL}/post_current_product?product_name={product_name}")
    return render_template('checkout.html')

@app.route('/clear_current_product', methods=['POST'])
def clear_current_product():
    response = requests.post(f"{PRODUCTS_URL}/clear_current_product")
    return response.json(), response.status_code

@app.route('/post_current_product', methods=['POST'])
def post_current_product():
    product_name = request.args.get('product_name')
    response = requests.post(f"{PRODUCTS_URL}/post_current_product?product_name={product_name}")
    return response.json(), response.status_code

@app.route('/fetch_current_product', methods=['GET'])
def fetch_current_product():
    response = requests.get(f"{PRODUCTS_URL}/fetch_current_product")
    return response.json(), response.status_code

@app.route('/post_order')
def post_order():
    response = requests.get(f"{USERS_URL}/authed_user")
    user_name = response.json().get('user_name')
    response = requests.get(f"{PRODUCTS_URL}/fetch_current_product")
    product_name = response.json().get('product_name')
    size = request.args.get('size')
    quantity = request.args.get('quantity')
    response = requests.post(f"{ORDERS_URL}/post_order?product_name={product_name}&user_name={user_name}&size={size}&quantity={quantity}")
    requests.post(f"{PRODUCTS_URL}/clear_current_product")
    return jsonify("Order Placed Successfully")


@app.route('/test')
def send_get_request():
    url = "http://localhost:5004/authed_user"  # Change the URL if your Flask app is running on a different host or port
    try:
        response = requests.get(url)
        if response.status_code == 201:
            print("User authenticated successfully")
            return jsonify("Response:", response.json())  # Assuming the response is in JSON format
        else:
            print("Not logged in successfully or session expired")
            print("Response:", response.text)
    except requests.exceptions.RequestException as e:
        print("Error:", e)
    return jsonify("not okay")

@app.route('/test1')
def send_get_request1():
    url = ":5004/authed_user"  # Change the URL if your Flask app is running on a different host or port
    try:
        response = requests.get(url)
        if response.status_code == 201:
            print("User authenticated successfully")
            return jsonify("Response:", response.json())  # Assuming the response is in JSON format
        else:
            print("Not logged in successfully or session expired")
            print("Response:", response.text)
    except requests.exceptions.RequestException as e:
        print("Error:", e)
    return jsonify("not okay")

@app.route('/test2')
def send_get_request2():
    url = "/authed_user"  # Change the URL if your Flask app is running on a different host or port
    try:
        response = requests.get(url)
        if response.status_code == 201:
            print("User authenticated successfully")
            return jsonify("Response:", response.json())  # Assuming the response is in JSON format
        else:
            print("Not logged in successfully or session expired")
            print("Response:", response.text)
    except requests.exceptions.RequestException as e:
        print("Error:", e)
    return jsonify("not okay")

@app.route('/test3')
def send_get_request3():
    url = "http://users-service:5004/authed_user"  # Change the URL if your Flask app is running on a different host or port
    try:
        response = requests.get(url)
        if response.status_code == 201:
            print("User authenticated successfully")
            return jsonify("Response:", response.json())  # Assuming the response is in JSON format
        else:
            print("Not logged in successfully or session expired")
            print("Response:", response.text)
    except requests.exceptions.RequestException as e:
        print("Error:", e)
    return jsonify("not okay")

@app.route('/logintest')
def test_page():
    # if session['user_authenticated'] == True:
    #     return redirect('/home')
    return render_template('test.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5001,debug=True,threaded=True)
