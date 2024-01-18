import json
import re
import urllib.parse
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from pathlib import Path

from httpx import Client, Cookies
from parsel import Selector

from freelancer_projects.consts import MONTHS_TRANSLATED


class Website(ABC):
    def __init__(self, cookies):
        self.cookies = Cookies()
        for cookie in json.load(open(Path(cookies).absolute())):
            self.cookies.set(cookie['name'], cookie['value'], cookie['domain'])

    @abstractmethod
    def have_unread_messages(self):
        raise NotImplementedError()

    @abstractmethod
    def get_projects(self):
        raise NotImplementedError()


class NineNineFreelas(Website):
    def __init__(self):
        super().__init__('99freelas-cookies.json')

    def have_unread_messages(self):
        with Client(cookies=self.cookies) as client:
            response = client.get('https://www.99freelas.com.br/dashboard')
            new_messages_uri = re.findall(
                r'NineNineFreelas\.infoUsuario\.novasMensagens = JSON\.parse\(decodeURIComponent\((.+?)\)',
                response.text,
                re.DOTALL,
            )[0]
            new_messages = urllib.parse.unquote(new_messages_uri)
            return bool(re.findall(r'"visualizada":false', new_messages))

    def get_projects(self):
        with Client(cookies=self.cookies) as client:
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
                        + timedelta(
                            milliseconds=project_milliseconds, hours=-3
                        ),
                    }
                )
            return result


class Workana(Website):
    def __init__(self):
        super().__init__('workana-cookies.json')

    def have_unread_messages(self):
        return False

    def get_projects(self):
        with Client(cookies=self.cookies) as client:
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
