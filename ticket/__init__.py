from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


db = SQLAlchemy() 
bcrypt = Bcrypt()


def create_app(test_config=None):
    app = Flask(__name__)
       
    app.config["SECRET_KEY"] = b'&\xab\x84$\xa5\t\x00Zs\x96\xcf\xaa\xf2\xd3\xebZ'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
   

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'authenticate.login'
    login_manager.init_app(app) 
    from . import model
    @login_manager.user_loader
    def load_user(user_id):
        return model.User.query.get(int(user_id))
    

    
    from . import main
    from . import authenticate
    from . import manager
    app.register_blueprint(main.blue)
    app.register_blueprint(authenticate.blue)
    app.register_blueprint(manager.blue)

    with app.app_context():
        db.create_all()
        db.session.commit()

    return app

