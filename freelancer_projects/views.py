from math import ceil

from flask import abort, render_template, request
from sqlalchemy import select

from freelancer_projects.config import get_config
from freelancer_projects.database import Session
from freelancer_projects.models import Project


def init_app(app, nine_nine_freelas, workana):
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
            projects = projects[
                pagination * (page - 1) : pagination * (page - 1) + pagination
            ]
            return render_template(
                'index.html',
                projects=projects,
                page=page,
                last_page=last_page,
                have_nine_nine_freelas_unread_messages=nine_nine_freelas.have_unread_messages(),
                have_workana_unread_messages=workana.have_unread_messages(),
            )
