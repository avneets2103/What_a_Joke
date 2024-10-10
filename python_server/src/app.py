from flask import Flask, jsonify
from flask_cors import CORS
from routes.user_route import user_bp 
from werkzeug.middleware.proxy_fix import ProxyFix

# Initialize Flask app
app = Flask(__name__)

# Middleware setup
CORS(app)

# Static files
app.wsgi_app = ProxyFix(app.wsgi_app)  # Equivalent to serving static files
app.static_folder = 'public'

# Register user routes
app.register_blueprint(user_bp, url_prefix="/api/v1/auth")