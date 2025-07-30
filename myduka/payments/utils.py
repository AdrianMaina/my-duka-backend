# =======================================================================
# FILE: myduka/payments/utils.py (NEW)
# =======================================================================
import requests
import base64
from datetime import datetime
from decouple import config

def get_mpesa_access_token():
    consumer_key = config('MPESA_CONSUMER_KEY')
    consumer_secret = config('MPESA_CONSUMER_SECRET')
    api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    
    r = requests.get(api_URL, auth=(consumer_key, consumer_secret))
    print("DEBUG: Access Token Response:", r.json())
    return r.json().get('access_token')

def lipa_na_mpesa_online(phone_number, amount, account_reference, transaction_desc, callback_url):
    access_token = get_mpesa_access_token()
    if not access_token:
        return {"error": "No access token returned."}

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    shortcode = config('MPESA_SHORTCODE')
    passkey = config('MPESA_PASSKEY')
    password = base64.b64encode((shortcode + passkey + timestamp).encode()).decode('utf-8')

    print("DEBUG: STK Payload")
    print({
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "Amount": amount,
        "PhoneNumber": phone_number,
        "CallBackURL": callback_url,
        "AccountReference": account_reference,
        "TransactionDesc": transaction_desc
    })

    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    response = requests.post(api_url, json={
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": shortcode,
        "PhoneNumber": phone_number,
        "CallBackURL": callback_url,
        "AccountReference": account_reference,
        "TransactionDesc": transaction_desc
    }, headers=headers)

    print("DEBUG: STK Response:", response.status_code, response.text)
    return response.json()
