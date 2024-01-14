from flask import render_template

from freelancer_projects.api import (get_nine_nine_freelas_projects,
                                     get_workana_projects)


def init_app(app):
    @app.get('/')
    def index():
        projects = get_nine_nine_freelas_projects()
        projects.extend(get_workana_projects())
        projects.sort(key=lambda p: p['datetime'])
        return render_template('index.html', projects=projects[::-1])
