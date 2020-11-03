from flask import Flask
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

from rpc_proxy.logger import create_logger
from rpc_proxy.tunnel import tunnel

app = None

app_logger = create_logger('proxy')


def __flask_setup():
    global app

    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.logger = app_logger
    CORS(app)

    @app.route("/", methods=["POST"])
    def index():
        return tunnel()


def __run_dev_server():
    app.config['DEVELOPMENT'] = True
    app.config['DEBUG'] = True

    app.run(host='127.0.0.1', port=8089)


__flask_setup()


def main():
    __run_dev_server()
