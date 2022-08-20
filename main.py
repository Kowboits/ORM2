import sqlalchemy
import json

from sqlalchemy.orm import declarative_base, relationship, sessionmaker

from models import create_tables, Stock, Book, Publisher, Sale, Shop

def search_publisher(session, name=None, id=None):
    if id is not None:
        result = session.query(Publisher).filter(Publisher.id == id).all()
        return result

    if name is not None:
        result = []
        for c in session.query(Publisher).filter(Publisher.name == name).all():
            result.append(c)
        return result

def data_loader(session):
    with open('test_data.json', 'r') as fd:
        data = json.load(fd)

    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()


DSN = "postgresql://postgres:postgres@localhost:5432/netology_orm"
engine = sqlalchemy.create_engine(DSN)

# create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

# data_loader(session)

requ = input('Введите ID или название автора:')
if requ.isdigit():
    print(*search_publisher(session, id=requ))
else:
    print(*search_publisher(session, name=requ))

session.close()


