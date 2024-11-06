from flask import Flask, request, jsonify, render_template
import requests
import base64

app = Flask(__name__)

# Base URL and client credentials
base_url = "https://simba-sbx-api.blocks.simbachain.com/"
client_id = "ckrL4IBXsep4zk0WvhTL5nR6TvBL2TQjXmuqFqTv"
client_secret = "0wbO8jQVVTqeloV3gp73IxC6v3iQS1ILTxR3dfdit8wutZtuK4hh1uglZN5iNqzUyU63ySvkeroXIzIIKIKZ7GlXpzLm5u4HoMQi9dDTDfcPkcw9p7LeplsVAFVcho39"
token = ""

# Function to get token
#@app.route('/')
def get_token(): #
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
    token = get_token()
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
    data = {"name": member_name, "member_id": member_id}
    response = requests.post(f"{base_url}v2/apps/IST408-608_simba_lab/contract/simba_lab/member_register/", headers=headers, json=data)
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
    response = requests.post(f"{base_url}v2/apps/IST408-608_simba_lab/contract/simba_lab/new_book/", headers=headers, json=data)
    return jsonify(response.json())

@app.route('/api/get_book', methods=['GET'])
def api_get_book():
    token = request.headers.get("Authorization")
    ISBN = request.args.get("ISBN")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.get(f"{base_url}v2/apps/IST408-608_simba_lab/contract/simba_lab/get_book/?ISBN={ISBN}", headers=headers)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)
