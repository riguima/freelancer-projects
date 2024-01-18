from threading import Thread
from time import sleep

from flask import Flask
from sqlalchemy import select

from freelancer_projects import views
from freelancer_projects.api import NineNineFreelas, Workana
from freelancer_projects.config import get_config
from freelancer_projects.database import Session
from freelancer_projects.models import Project

nine_nine_freelas = NineNineFreelas()
workana = Workana()


def add_projects():
    while True:
        projects = nine_nine_freelas.get_projects()
        projects.extend(workana.get_projects())
        with Session() as session:
            for project in projects:
                query = select(Project).where(Project.url == project['url'])
                project_model = session.scalars(query).first()
                if project_model is None:
                    project_model = Project(
                        title=project['title'],
                        url=project['url'],
                        project_datetime=project['datetime'],
                    )
                    session.add(project_model)
                    session.commit()
            for project in session.scalars(
                select(Project).order_by(Project.project_datetime.desc())
            ).all()[get_config()['MAX_PROJECTS'] :]:
                session.delete(project)
                session.commit()
        sleep(60)


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    Thread(target=add_projects).start()
    views.init_app(app, nine_nine_freelas, workana)
    return app


app = create_app()
