import firebase_admin
from firebase_admin import credentials, db

# 🔹 Firebase Initialization (Ensure it's only initialized once)
if not firebase_admin._apps:
    cred = credentials.Certificate("/Users/amani/Desktop/HAIL_APP/scammer-detection-app-firebase-adminsdk-fbsvc-154eea897a.json")
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://scammer-detection-app-default-rtdb.firebaseio.com/"
    })

# 🔹 Firebase Functions
def add_scam_message(message, label="spam"):
    """Add a new scam message to Firebase."""
    ref = db.reference("spam_messages")
    new_message_ref = ref.push()
    new_message_ref.set({"message": message, "label": label})
    return True

def is_scam_number(phone_number):
    """Check if a phone number is reported as a scam."""
    ref = db.reference("scam_numbers")
    return phone_number in ref.get() if ref.get() else False

def add_scam_number(phone_number):
    """Add a scam phone number to Firebase."""
    ref = db.reference("scam_numbers")
    ref.update({phone_number: True})
    return True

def is_scam_link(url):
    """Check if a URL is reported as a scam."""
    ref = db.reference("scam_links")
    return url in ref.get() if ref.get() else False

def add_scam_link(url):
    """Add a scam URL to Firebase."""
    ref = db.reference("scam_links")
    ref.update({url: True})
    return True
