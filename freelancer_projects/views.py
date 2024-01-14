from flask import render_template
from sqlalchemy import select

from freelancer_projects.api import (get_nine_nine_freelas_projects,
                                     get_workana_projects)
from freelancer_projects.database import Session
from freelancer_projects.models import Project
from freelancer_projects.config import get_config


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
                    project_model = Project(
                        title=project['title'],
                        url=project['url'],
                        project_datetime=project['datetime'],
                    )
                    session.add(project_model)
                    session.commit()
            for project in already_added_projects:
                projects.remove(project)
            for project in session.scalars(select(Project).order_by(Project.project_datetime.desc())).all()[get_config()['MAX_PROJECTS']:]:
                session.delete(project)
                session.commit()
            return render_template(
                'index.html',
                projects=session.scalars(
                    select(Project).order_by(Project.project_datetime.desc())
                ),
            )
