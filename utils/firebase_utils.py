import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("firebase-credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def get_user_terms_acceptance(user_id):
    doc = db.collection("users").document(user_id).get()
    return doc.exists and doc.to_dict().get("terms_accepted", False)

def set_user_terms_acceptance(user_id, accepted=True):
    db.collection("users").document(user_id).set({"terms_accepted": accepted}, merge=True)

def save_user_interaction(user_id, data: dict):
    """Store {'user': str} or {'bot': str} with a timestamp."""
    db.collection("users") \
      .document(user_id) \
      .collection("chats") \
      .add({**data, "timestamp": firestore.SERVER_TIMESTAMP})

def get_recent_interactions(user_id, limit=5):
    """Get recent interactions for context"""
    docs = db.collection("users") \
             .document(user_id) \
             .collection("chats") \
             .order_by("timestamp", direction=firestore.Query.DESCENDING) \
             .limit(limit) \
             .stream()
    
    interactions = []
    for doc in docs:
        interactions.append(doc.to_dict())
    
    return interactions