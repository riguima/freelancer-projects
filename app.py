from flask import Flask

from freelancer_projects import views


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    views.init_app(app)
    return app


app = create_app()
