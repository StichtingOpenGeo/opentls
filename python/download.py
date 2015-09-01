import requests

CLIENT_ID     = "nmOIiEJO5khvtLBK9xad3UkkS8Ua"
CLIENT_SECRET = "FE8ef6bVBiyN0NeyUJ5VOWdelvQa"

def get_token(username, password, client_id=CLIENT_ID, client_secret=CLIENT_SECRET):
    post_data = {"username": username,
                 "password": password,
                 "client_id": client_id,
                 "client_secret": client_secret,
                 "grant_type": "password",
                 "scope": "openid"}

    return requests.post("https://login.ov-chipkaart.nl/oauth2/token", data = post_data).json()

def refresh_token(refresh_token, client_id=CLIENT_ID, client_secret=CLIENT_SECRET):
    post_data = {"refresh_token": refresh_token,
                 "client_id": client_id,
                 "client_secret": client_secret,
                 "grant_type": "refresh_token"}

    return requests.post("https://login.ov-chipkaart.nl/oauth2/token", data = post_data).json()

def get_authorization(id_token):
    post_data = {"authenticationToken": id_token}

    response = requests.post("https://api2.ov-chipkaart.nl/femobilegateway/v1/api/authorize", data = post_data)
    as_json = response.json()
    return as_json['o']

def get_cards_list(authorizationToken, locale="nl-NL"):
    post_data = {"authorizationToken": authorizationToken,
                 "locale": locale}

    response = requests.post("https://api2.ov-chipkaart.nl/femobilegateway/v1/cards/list", data = post_data)
    as_json = response.json()
    return as_json['o']

def get_transaction_list(authorizationToken, mediumId, offset = 0, locale="nl-NL"):
    transactions = []

    post_data = {"authorizationToken": authorizationToken,
                 "mediumId": mediumId,
                 "offset": offset,
                 "locale": locale}

    response = requests.post("https://api2.ov-chipkaart.nl/femobilegateway/v1/transaction/list", data = post_data)
    as_json = response.json()
    transactions += as_json['o']['records']

    while offset < as_json['o']['nextOffset']:
        post_data['offset'] = as_json['o']['nextOffset']
        response = requests.post("https://api2.ov-chipkaart.nl/femobilegateway/v1/transaction/list", data = post_data)
        as_json = response.json()
        transactions += as_json['o']['records']
        offset = int(as_json['o']['nextOffset'])

    return transactions

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print "Usage: download.py username password"
        sys.exit(-1)

    oauth = get_token(sys.argv[1], sys.argv[2])
    if 'id_token' not in oauth:
        print oauth
        sys.exit(-1)

    # oauth = refresh_token(oauth['refresh_token'])

    authorizationToken = get_authorization(oauth['id_token'])
    cards = get_cards_list(authorizationToken)

    for card in cards:
        records = get_transaction_list(authorizationToken, card['mediumId'])
        for record in records:
            del record['transactionExplanation']
            del record['ePurseMutInfo']
            record['transactionDateTime'] = (record['transactionDateTime'] / 1000) * 1000

        card['transactions'] = records

    import json
    print json.dumps(cards)
