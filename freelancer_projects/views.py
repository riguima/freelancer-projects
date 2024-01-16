from flask import render_template, request
from sqlalchemy import select

from freelancer_projects.config import get_config
from freelancer_projects.database import Session
from freelancer_projects.models import Project


def init_app(app):
    @app.get('/')
    def index():
        with Session() as session:
            projects = session.scalars(
                select(Project).order_by(Project.project_datetime.desc())
            ).all()
            page = int(request.args.get('page', 1))
            return render_template(
                'index.html',
                projects=projects,
                page=page,
                last_page=len(projects) // get_config()['PAGINATION'],
            )
