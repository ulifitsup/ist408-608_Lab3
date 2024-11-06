from flask import Flask, request, jsonify, render_template
import requests
import base64

app = Flask(__name__)

# Base URL and client credentials
base_url = "https://simba-sbx-api.blocks.simbachain.com/"
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"

# Function to get token
def get_token():
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

@app.route('/member_register', methods=['POST'])
def member_register():
    token = get_token()
    member_name = request.form.get("member_name")
    member_id = request.form.get("member_id")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {"name": member_name, "member_id": member_id}
    response = requests.post(f"{base_url}v2/apps/IST408-608_simba_lab/contract/simba_lab/member_register/", headers=headers, json=data)
    return jsonify(response.json())

@app.route('/new_book', methods=['POST'])
def new_book():
    token = get_token()
    book_name = request.form.get("book_name")
    ISBN = request.form.get("ISBN")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {"book_name": book_name, "ISBN": ISBN}
    response = requests.post(f"{base_url}v2/apps/IST408-608_simba_lab/contract/simba_lab/new_book/", headers=headers, json=data)
    return jsonify(response.json())

@app.route('/get_book', methods=['GET'])
def get_book():
    token = get_token()
    ISBN = request.args.get("ISBN")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.get(f"{base_url}v2/apps/IST408-608_simba_lab/contract/simba_lab/get_book/?ISBN={ISBN}", headers=headers)
    return jsonify(response.json())

# More routes for other endpoints can be added here...

if __name__ == '__main__':
    app.run(debug=True)
