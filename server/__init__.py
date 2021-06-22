from flask import Flask, Blueprint
from flask_cors import CORS

from .configs import BaseConfigs, api


def create_app(config: BaseConfigs = BaseConfigs) -> Flask:
    """Return Flask app for project initialization."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)
    blueprint: Blueprint = Blueprint("api", __name__, url_prefix="/api")
    CORS(app, resources=r'/api/*', supports_credentials=True)
    init_lazily(blueprint)
    app.register_blueprint(blueprint)
    init_routes()
    return app


def init_lazily(blueprint: Blueprint) -> None:
    """Lazy init."""
    api.init_app(blueprint)


def init_routes() -> None:
    """Init Routes by using namespaces."""
    from .views import namespace
    api.add_namespace(namespace)


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0")
