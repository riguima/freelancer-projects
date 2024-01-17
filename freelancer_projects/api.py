import json
import re
from datetime import datetime, timedelta
from pathlib import Path

from httpx import Client, Cookies
from parsel import Selector

from freelancer_projects.consts import MONTHS_TRANSLATED


def get_nine_nine_freelas_projects():
    with Client() as client:
        response = client.get('https://www.99freelas.com.br/projects')
        selector = Selector(response.text)
        result = []
        for project in selector.css('.result-item'):
            project_link = project.css('.title a')
            project_milliseconds = int(
                project.css('.datetime').attrib['cp-datetime']
            )
            result.append(
                {
                    'title': project_link.css('::text').get(),
                    'url': 'https://www.99freelas.com.br'
                    + project_link.attrib['href'],
                    'datetime': datetime(year=1970, month=1, day=1)
                    + timedelta(milliseconds=project_milliseconds, hours=-3),
                }
            )
        return result


def get_workana_projects():
    cookies = Cookies()
    for cookie in json.load(open(Path('workana-cookies.json').absolute())):
        cookies.set(cookie['name'], cookie['value'], cookie['domain'])
    with Client(cookies=cookies) as client:
        response = client.get('https://www.workana.com/jobs?language=pt')
        selector = Selector(response.text)
        result = []
        for project in selector.css('.project-item'):
            project_datetime = project.css(
                '.project-main-details .date'
            ).attrib['title']
            month = re.findall(r'de (.+?) de', project_datetime)[0]
            project_datetime = datetime.strptime(
                project_datetime.replace(month, MONTHS_TRANSLATED[month]),
                '%d de %B de %Y %H:%M',
            )
            project_link = project.css('.project-title a')
            result.append(
                {
                    'title': project_link.css('::text').get(),
                    'url': 'https://www.workana.com'
                    + project_link.attrib['href'],
                    'datetime': project_datetime,
                }
            )
        return result
