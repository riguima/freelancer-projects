from flask import render_template

from freelancer_projects.database import Session
from freelancer_projects.models import Project
from freelancer_projects.api import (get_nine_nine_freelas_projects,
                                     get_workana_projects)

from sqlalchemy import select


def init_app(app):
    @app.get('/')
    def index():
        projects = get_nine_nine_freelas_projects()
        projects.extend(get_workana_projects())
        already_added_projects = []
        with Session() as session:
            for project in projects:
                query = select(Project).where(Project.url == project['url'])
                project_model = session.scalars(query).first()
                if project_model:
                    already_added_projects.append(project)
                else:
                    project_model = Project(title=project['title'], url=project['url'], project_datetime=project['datetime'])
                    session.add(project_model)
                    session.commit()
            for project in already_added_projects:
                projects.remove(project)
            return render_template('index.html', projects=session.scalars(select(Project).order_by(Project.project_datetime.desc())))
