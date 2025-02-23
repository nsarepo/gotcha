from firebase_utils import db
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# 🔹 Load Spam Data
def get_all_spam_messages():
    """Fetch all spam messages from Firebase."""
    ref = db.reference("spam_messages")
    data = ref.get()
    
    if not data:
        return []

    return [{"id": key, "label": value["label"], "message": value["message"]} for key, value in data.items()]

def load_spam_data():
    ref = db.reference("spam_messages")
    data = ref.get()
    print("🔹 Raw Firebase Data:", data)  # Debugging line

    messages, labels = [], []

    if isinstance(data, dict):
        for key, value in data.items():
            print(f"🔹 Processing {key}: {value}")  # Debugging line
            if isinstance(value, dict):
                # Convert keys to lowercase
                normalized_value = {str(k).lower(): v for k, v in value.items()}
                msg = str(normalized_value.get("message", "")).strip()
                lbl = str(normalized_value.get("label", "")).strip()
                
                if msg and lbl:
                    messages.append(msg)
                    labels.append(lbl)

    print("✅ Messages:", messages)  # Debugging line
    print("✅ Labels:", labels)  # Debugging line
    return messages, labels

# 🔹 Train Spam Detection Model
X, Y = load_spam_data()
if not X or not Y:
    print("⚠ Warning: No training data found in Firebase.")
    cv, model = None, None
else:
    cv = CountVectorizer(stop_words="english")
    X_train = cv.fit_transform(X)
    model = MultinomialNB()
    model.fit(X_train, Y)

def predict_spam(message):
    """Predict if a message is spam or not."""
    if not model or not cv:
        return "Error: Model not trained."
    
    input_message = cv.transform([message]).toarray()
    result = model.predict(input_message)
    return result[0]

def check_spam_message(message):
    """Check if a message is spam."""
    return predict_spam(message) if model else "Error: Model not trained."

# 🔹 Add New Spam Message to Firebase
def add_scam_message(message, label="spam"):
    """Add a new scam message in the correct Firebase format (msg0, msg1, ...)."""
    ref = db.reference("spam_messages")
    
    # Generate new unique key in "msgn" format
    existing_keys = list(ref.get().keys()) if ref.get() else []
    next_index = len(existing_keys)
    new_key = f"msg{next_index}"
    
    ref.child(new_key).set({
        "label": label,
        "message": message
    })
    
    return new_key  # Return the unique key
