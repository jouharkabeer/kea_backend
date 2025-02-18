import firebase_admin
from firebase_admin import credentials, auth

# Load Firebase credentials
cred = credentials.Certificate("config/keabackend-firebase-adminsdk-fbsvc-fa14689b0b.json")  
firebase_admin.initialize_app(cred)
