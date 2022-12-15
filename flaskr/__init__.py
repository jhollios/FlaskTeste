import os
from flask import Flask


def create_app(test_config=None):
    # cria e configura a aplicação
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )

    if test_config is None:
        # carregar a instância config, caso ela exista, quando não estiver testando
        app.config.from_pyfile('config.py', silent=True)
    else:
        # carregar o test config caso tenha passado
        app.config.from_mapping(test_config)

    # garantir que o diretório da instância exista
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # uma simples página que diz olá
    @app.route('/hello')
    def hello():
        return 'Olá, mundo!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    return app
