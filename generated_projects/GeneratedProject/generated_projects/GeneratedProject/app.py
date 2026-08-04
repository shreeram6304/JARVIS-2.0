import os
from flask import Flask, render_template
from calculator.routes import api_bp

def create_app() -> Flask:
    """Application factory for Flask app configuration."""
    app = Flask(__name__)
    
    # Secret key configuration
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "prod_calculator_secret_key_123")

    # Register API blueprints
    app.register_blueprint(api_bp)

    @app.route("/")
    def index():
        return render_template("index.html")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)