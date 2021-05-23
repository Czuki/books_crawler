from sqlalchemy import create_engine, Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, Text, VARCHAR
from scrapy.utils.project import get_project_settings

Base = declarative_base()


def db_connect():
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table(engine):
    Base.metadata.create_all(engine)


class Book(Base):
    __tablename__ = 'librarian_book'

    id = Column(Integer, primary_key=True)
    name = Column('name', Text(), unique=True)
    isbn = Column(VARCHAR(64), unique=True)
    author_id = Column(Integer, ForeignKey('librarian_author.id'))


class Author(Base):
    __tablename__ = 'librarian_author'

    id = Column(Integer, primary_key=True)
    author = Column('author', VARCHAR(64), unique=True)
