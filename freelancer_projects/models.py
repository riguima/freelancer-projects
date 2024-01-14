from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

from freelancer_projects.database import db


class Base(DeclarativeBase):
    pass


class Project(Base):
    __tablename__ = 'projects'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    url: Mapped[str]
    project_datetime: Mapped[datetime]


Base.metadata.create_all(db)
