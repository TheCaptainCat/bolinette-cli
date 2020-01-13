from flask import Flask
from flask_cors import CORS

from bolinette import env, Namespace
from bolinette.database import init_db
from bolinette.jwt import init_jwt
from bolinette.routes import init_routes
from bolinette.documentation import init_docs
from bolinette.templating import paths


class Bolinette:
    def __init__(self, name, **options):
        self.cwd = paths.cwd()
        self.origin = paths.dirname(__file__)
        env_overrides = options.get('env', {})
        self.app = Flask(name, static_url_path='')
        CORS(self.app, supports_credentials=True)
        env.init(self.app, overrides=env_overrides)
        init_jwt(self.app)
        init_db(self.app)
        init_routes(self.app)
        init_docs(self.app)
        Namespace.init_namespaces(self.app)
    
    def instance_file(self, path):
        return None
