from flask import Flask, request, jsonify, render_template
import requests
import base64

app = Flask(__name__)

# Base URL and client credentials
base_url = "https://simba-sbx-api.blocks.simbachain.com"
base_endpoint = ""
#client_id = "ckrL4IBXsep4zk0WvhTL5nR6TvBL2TQjXmuqFqTv"
#client_secret = "0wbO8jQVVTqeloV3gp73IxC6v3iQS1ILTxR3dfdit8wutZtuK4hh1uglZN5iNqzUyU63ySvkeroXIzIIKIKZ7GlXpzLm5u4HoMQi9dDTDfcPkcw9p7LeplsVAFVcho39"

# Function to get token
def get_token(client_id, client_secret): #
    endpoint = '/o/token/'
    client = f"{client_id}:{client_secret}"
    encoded_credentials = base64.b64encode(client.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    response = requests.post(base_url + endpoint, headers=headers, data=data)
    return response.json().get('access_token')

# Define routes for the Flask app
@app.route('/')
def home():
    return render_template('home.html')  # Render a homepage with options

@app.route('/api/get_token', methods=['POST'])
def api_get_token():
    client_id = request.json.get("client_id")
    client_secret = request.json.get("client_secret")
    global base_endpoint
    base_endpoint = request.json.get("endpoint")
    
    token = get_token(client_id, client_secret)
    return jsonify({"access_token": token})

@app.route('/api/member_register', methods=['POST'])
def api_member_register():
    token = request.json.get("token")
    member_name = request.json.get("member_name")
    member_id = request.json.get("member_id")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    print(f"{base_url}{base_endpoint}member_register/")
    data = {"name": member_name, "member_id": member_id}
    response = requests.post(f"{base_url}{base_endpoint}member_register/", headers=headers, json=data)
    return jsonify(response.json())

@app.route('/api/member_deactive', methods=['POST'])
def api_member_deactive():
    token = request.json.get("token")
    member_id = request.json.get("member_id")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {"member_id": member_id}
    response = requests.post(f"{base_url}{base_endpoint}member_deactive/", headers=headers, json=data)
    return jsonify(response.json())

@app.route('/api/new_book', methods=['POST'])
def api_new_book():
    token = request.json.get("token")
    book_name = request.json.get("book_name")
    ISBN = request.json.get("ISBN")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {"book_name": book_name, "ISBN": ISBN}
    response = requests.post(f"{base_url}{base_endpoint}new_book/", headers=headers, json=data)
    return jsonify(response.json())

@app.route('/api/book_borrow', methods=['POST'])
def api_book_borrow():
    token = request.json.get("token")
    member_id = request.json.get("member_id")
    ISBN = request.json.get("ISBN")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {"member_id": member_id, "ISBN": ISBN}
    response = requests.post(f"{base_url}{base_endpoint}borrow_book/", headers=headers, json=data)
    return jsonify(response.json())

@app.route('/api/book_return', methods=['POST'])
def api_book_return():
    token = request.json.get("token")
    member_id = request.json.get("member_id")
    ISBN = request.json.get("ISBN")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {"member_id": member_id, "ISBN": ISBN}
    response = requests.post(f"{base_url}{base_endpoint}return_book/", headers=headers, json=data)
    return jsonify(response.json())

@app.route('/api/get_book', methods=['GET'])
def api_get_book():
    token = request.headers.get("Authorization")
    ISBN = request.args.get("ISBN")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.get(f"{base_url}{base_endpoint}get_book/?ISBN={ISBN}", headers=headers)
    return jsonify(response.json())

@app.route('/api/get_member', methods=['GET'])
def api_get_member():
    token = request.headers.get("Authorization")
    member_id = request.args.get("member_id")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {"member_id": member_id}
    response = requests.get(f"{base_url}{base_endpoint}get_member/?member_id={member_id}", headers=headers)
    return jsonify(response.json())


if __name__ == '__main__':
    app.run(debug=True)
