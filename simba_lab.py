import requests
import json
import base64
from flask import Flask

base_url = "https://simba-sbx-api.blocks.simbachain.com/"
token = ""

simba_lab = Flask(__name__)

@simba_lab.route('/')

def get_token(client_id, client_secret): #
    endpoint = '/o/token/'
    client = f"{client_id}:{client_secret}"
    #client = "ckrL4IBXsep4zk0WvhTL5nR6TvBL2TQjXmuqFqTv:0wbO8jQVVTqeloV3gp73IxC6v3iQS1ILTxR3dfdit8wutZtuK4hh1uglZN5iNqzUyU63ySvkeroXIzIIKIKZ7GlXpzLm5u4HoMQi9dDTDfcPkcw9p7LeplsVAFVcho39"
    encoded_credentials = base64.b64encode(client.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
    "grant_type": "client_credentials"
    }
    response = requests.post(base_url + endpoint, headers=headers, data=data)
    access_token = response.json()['access_token']
    globals.token = access_token

    return(access_token)

def member_register(member_name, member_id): 
    token = get_token()
    endpoint = "v2/apps/IST408-608_simba_lab/contract/simba_lab/member_register/"

    headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
    }

    data = {
        "name" : member_name,
        "member_id" : member_id
    }

    response = requests.post(base_url + endpoint, headers=headers, json=data)
    return(response.json()) # Later specify the return

def member_deactive(member_id): #
    token = get_token()
    endpoint = "v2/apps/IST408-608_simba_lab/contract/simba_lab/member_deactive/"

    headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
    }

    data = {
        "member_id" : member_id
    }

    response = requests.post(base_url + endpoint, headers=headers, json=data)
    return(response.json()) # Later specify the return

def new_book(book_name, ISBN):
    token = get_token()
    endpoint = "v2/apps/IST408-608_simba_lab/contract/simba_lab/new_book/"

    headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
    }

    data = {
        "book_name" : book_name,
        "ISBN" : ISBN
    }

    response = requests.post(base_url + endpoint, headers=headers, json=data)
    return(response.json()) # Later specify the return

def borrow_book(member_id, ISBN):
    token = get_token()
    endpoint = "v2/apps/IST408-608_simba_lab/contract/simba_lab/borrow_book/"

    headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
    }

    data = {
        "member_id" : member_id,
        "ISBN" : ISBN
    }

    response = requests.post(base_url + endpoint, headers=headers, json=data)
    return(response.json()) # Later specify the return

def return_book(member_id, ISBN):
    token = get_token()
    endpoint = "v2/apps/IST408-608_simba_lab/contract/simba_lab/return_book/"

    headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
    }

    data = {
        "member_id" : member_id,
        "ISBN" : ISBN
    }

    response = requests.post(base_url + endpoint, headers=headers, json=data)
    return(response.json()) # Later specify the return

def get_book(ISBN):
    token = get_token()
    endpoint = f"v2/apps/IST408-608_simba_lab/contract/simba_lab/get_book/?ISBN={ISBN}"

    headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
    }

    response = requests.get(base_url + endpoint, headers=headers)
    return(response.json()) # Later specify the return

def get_member(member_id):
    token = get_token()
    endpoint = f"v2/apps/IST408-608_simba_lab/contract/simba_lab/get_member/?member_id={member_id}"

    headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
    }

    response = requests.get(base_url + endpoint, headers=headers)
    return(response.json()) # Later specify the return

if __name__ == '__main__':
    simba_lab.run(debug=True)