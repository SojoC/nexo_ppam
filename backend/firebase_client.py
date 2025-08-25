import os
import firebase_admin
from firebase_admin import credentials, auth, firestore

cred_path = os.getenv("FIREBASE_CREDENTIALS", "/keys/firebase.json")

if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def create_user(email, password):
    """Crear un usuario en Firebase Auth"""
    user = auth.create_user(email=email, password=password)
    return user.uid

def get_user(uid):
    """Obtener datos de un usuario"""
    return auth.get_user(uid)

def save_message(user_id, message):
    """Guardar un mensaje en Firestore"""
    db.collection("messages").add({
        "user_id": user_id,
        "message": message
    })
