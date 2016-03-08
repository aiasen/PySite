from flask import Flask
from flask.ext.bootstrap import Bootstrap
# from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.pagedown import PageDown
from config import config

bootstrap = Bootstrap()
# mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__, static_url_path='', static_folder='/home/wangkui/p/flasky/app/static')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    # mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask.ext.sslify import SSLify
        sslify = SSLify(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .user import user as user_blueprint, user_np as user_np_blueprint
    app.register_blueprint(user_np_blueprint, url_prefix='/u')  # /u/<username>
    app.register_blueprint(user_blueprint, url_prefix='/user')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .resource import image as image_blueprint, upload as upload_blueprint
    app.register_blueprint(image_blueprint, url_prefix='/img')
    app.register_blueprint(upload_blueprint, url_prefix='/upload')

    from .blog import blog as blog_blueprint
    app.register_blueprint(blog_blueprint, url_prefix='/blog')

    from .movie import movie as movie_blueprint
    app.register_blueprint(movie_blueprint, url_prefix='/movie')

    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    return app