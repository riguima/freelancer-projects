from flask import render_template, request, abort
from sqlalchemy import select
from math import ceil

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
            pagination = get_config()['PAGINATION']
            last_page = ceil(len(projects) / pagination)
            if page > last_page:
                return abort(404)
            projects = projects[pagination * (page - 1):pagination * (page - 1) + pagination]
            return render_template(
                'index.html',
                projects=projects,
                page=page,
                last_page=last_page,
            )
