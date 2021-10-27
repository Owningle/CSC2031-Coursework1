# IMPORTS
import imp
import socket
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.exceptions import HTTPException

# CONFIG
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lottery.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'LongAndRandomSecretKey'

# initialise database
db = SQLAlchemy(app)


# HOME PAGE VIEW
@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(HTTPException)
def handle_exception(e):
    return render_template('error.html', error = e)


if __name__ == "__main__":
    my_host = "127.0.0.1"
    free_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    free_socket.bind((my_host, 0))
    free_socket.listen(5)
    free_port = free_socket.getsockname()[1]
    free_socket.close()

    login_manager = LoginManager()
    login_manager.login_view = 'users.login'
    login_manager.init_app(app)

    from models import User

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # BLUEPRINTS
    # import blueprints
    from users.views import users_blueprint
    from admin.views import admin_blueprint
    from lottery.views import lottery_blueprint

    # register blueprints with app
    app.register_blueprint(users_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(lottery_blueprint)

    app.run(host=my_host, port=5000, debug=True)