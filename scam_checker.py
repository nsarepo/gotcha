import requests
from config import NUMVERIFY_API_KEY, URLSCAN_API_KEY
from firebase_utils import is_scam_number, is_scam_link

def check_phone_number(phone_number):
    """Check if a phone number is a scam using NumVerify API and Firebase."""
    if is_scam_number(phone_number):
        return "High risk - This number is reported as a scammer!"

    url = f"http://apilayer.net/api/validate?access_key={NUMVERIFY_API_KEY}&number={phone_number}"
    try:
        response = requests.get(url)
        data = response.json()

        if not data.get("valid"):
            return "Invalid phone number."
        if data.get("line_type") == "voip" or "Unknown" in data.get("carrier", ""):
            return "High risk - This number may be used by scammers!"
        if data.get("location") == "International" or "Prepaid" in data.get("carrier", ""):
            return "Medium risk - Be cautious."
        
        return "Low risk - No significant scam indicators detected."
    except requests.exceptions.RequestException as e:
        return f"Error analyzing phone number: {e}"

def check_high_risk_links(url):
    """Check if a URL is a scam using URLScan API and Firebase."""
    if is_scam_link(url):
        return {"message": "High risk - This URL is reported as a scam!"}

    headers = {"API-Key": URLSCAN_API_KEY, "Content-Type": "application/json"}
    data = {"url": url, "visibility": "public"}
    try:
        response = requests.post("https://urlscan.io/api/v1/scan/", headers=headers, json=data)
        response_data = response.json()
        result_url = response_data.get("result")

        return {"message": f"Scan submitted. Check results at: {result_url}"} if result_url else {"message": "Unable to scan the URL."}
    except requests.exceptions.RequestException as e:
        return {"message": f"Error scanning URL: {e}"}
