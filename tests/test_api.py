from httpx import get

from freelancer_projects.api import (get_nine_nine_freelas_projects,
                                     get_workana_projects)


def test_get_nine_nine_freelas_projects():
    projects = get_nine_nine_freelas_projects()
    assert len(projects) == 10
    for project in projects:
        assert get(project['url']).status_code == 200


def test_get_workana_projects():
    projects = get_workana_projects()
    assert len(projects) == 21
    for project in projects:
        assert get(project['url']).status_code == 200
