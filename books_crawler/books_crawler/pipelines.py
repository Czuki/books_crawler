# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .models import db_connect, create_table, Book, Author
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from .spiders.gandalf import GandalfSpider
from sqlalchemy import select


class BooksCrawlerPipeline:
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):

        session = self.Session()
        book = Book()
        author = Author()
        book.name = item['name']
        book.isbn = item['isbn']

        author.author = item['author']
        session.add(author)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()


        select_author_query = select(Author).where(Author.author == item['author'])
        author_id = session.execute(select_author_query).first()
        book.author_id = author_id['Author'].id
        session.add(book)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()

        session.close()

        return item
