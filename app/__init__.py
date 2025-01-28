from flask import Flask

app = Flask(__name__)  # Crée l'application Flask

# Importer les routes après avoir créé l'application
from app.routes import route
