import requests

API_URL = "https://sidebar.stract.to/api"
HEADERS = {"Authorization": "Bearer ProcessoSeletivoStract2025"}

def fetch_data(endpoint, params=None):
    response = requests.get(f"{API_URL}{endpoint}", headers=HEADERS, params=params)
    if response.status_code == 200:
        return response.json()
    return None

def get_platforms():
    return fetch_data("/platforms")

def get_accounts(platform):
    all_accounts = []
    page = 1
    while True:
        response = fetch_data(f"/accounts?platform={platform}", params={"page": page})
        if not response or "accounts" not in response:
            break
        all_accounts.extend(response["accounts"])
        if page >= response.get("pagination", {}).get("total", 1):
            break
        page += 1
    return {"accounts": all_accounts}

def get_fields(platform):
    all_fields = []
    page = 1
    while True:
        response = fetch_data(f"/fields?platform={platform}", params={"page": page})
        if not response or "fields" not in response:
            break
        all_fields.extend(response["fields"])
        if page >= response.get("pagination", {}).get("total", 1):
            break
        page += 1
    return {"fields": all_fields}

def get_insights(platform, account, token, fields, page=1):
    return fetch_data(
        f"/insights?platform={platform}&account={account}&token={token}&fields={fields}",
        params={"page": page}
    )