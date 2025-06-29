from flask import Flask
from flask_cors import CORS
from routes.auth_routes import init_auth_routes
from routes.model_routes import init_model_routes
from routes.analytics_routes import init_analytics_routes

app = Flask(__name__)
CORS(app)

# Initialize routes
app = init_auth_routes(app)
app = init_model_routes(app)
app = init_analytics_routes(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)