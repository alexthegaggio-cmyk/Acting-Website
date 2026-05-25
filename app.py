import os
from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", "fallback-dev-key-change-me")
    app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024  # 100 MB

    # Ensure uploads directory exists
    uploads_dir = os.path.join(app.static_folder, "uploads")
    os.makedirs(uploads_dir, exist_ok=True)

    # Initialise database
    from database import init_db
    init_db()

    # Register blueprints
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.modules import modules_bp
    from routes.certificate import certificate_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(modules_bp)
    app.register_blueprint(certificate_bp)

    # Index route
    @app.route("/")
    def index():
        return render_template("index.html")

    # Sitemap route
    @app.route("/sitemap")
    def sitemap():
        return render_template("sitemap.html")

    # Custom error handlers
    @app.errorhandler(404)
    def not_found(e):
        return render_template("base.html", error_code=404, error_message="Page not found"), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template("base.html", error_code=500, error_message="Internal server error"), 500

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5001)
